import os
import regex
import duckdb
import threading
import multiprocessing

from utils import *
from logger.log import get_logger

conn = duckdb.connect(database=os.environ.get('DUCKDB_PATH'), read_only=False)
thread_amount = int(os.environ.get('LOAD_THREAD_AMOUNT'))
log = get_logger('load_data')

def query(thread_id: int, sqls: str):
    cur = conn.cursor()
    cur.execute(''.join(sqls))
    log.debug(f"Thread {thread_id+1} executed {len(sqls)} queries")

def load(progress, path: str, file_extension: str, compiled_regex: str, table_prefix: str = ''):
    files = find_files(path, file_extension)
    log.info(f"Found {len(files)} files to process")
    log.debug(f"Files found: {files}")

    dirs = list({regex.search(pattern=compiled_regex, string=x).group(1) for x in files})
    batches = separate_files(files, compiled_regex)
    log.info(f"The files were separated in {len(batches)} batches, namely: {list(batches.keys())}")
    log.debug(f"Files in each batch: {batches}")

    log.info("Creating tables in DuckDB")
    create_sqls = []
    for dir in batches.keys():
        create_sqls.append(f"CREATE OR REPLACE TABLE {table_prefix}{dir} AS (SELECT * FROM '{batches[dir][0]}');")
    log.debug(create_sqls)
    conn.execute(''.join(create_sqls))

    log.info("Creating COPY queries for DuckDB ingestion")
    copy_sqls = []
    for dir in batches.keys():
        for i in range(1, len(batches[dir])):
            copy_sqls.append(f"COPY {table_prefix}{dir} FROM '{batches[dir][i]}' (FORMAT JSON, ARRAY true);")
    log.debug(copy_sqls)

    threads = []
    for i in range(thread_amount):

        start = i * len(files) // thread_amount
        end = (i + 1) * len(files) // thread_amount
        if i == thread_amount - 1:
            end = len(files)

        log.info(f"The thread {i+1} will process {start} to {end-1} queries")
        thread = threading.Thread(target=query, args=(i, copy_sqls[start:end]))
        threads.append(thread)

    log.info("Triggering queries in parallel")
    for thread in threads:
        thread.start()

    progress_bar_process = multiprocessing.Process(target=create_progress_bar, args=(progress_value, thread_amount))
    progress_bar_process.start()

    for thread in threads:
        thread.join()
        progress.value += 1

    progress_bar_process.join()
    log.info("All threads finished")

if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        log.info("Starting data loading to DuckDB...")

        log.info("{thread_amount} threads will be executed in parallel")
        progress_value = manager.Value('i', 0)

        load(
            path='./data/curated',
            file_extension='json',
            compiled_regex=regex.compile(os.environ.get('CURATED_REGEX')),
            progress=progress_value
        )

        log.info("Data loading completed")

