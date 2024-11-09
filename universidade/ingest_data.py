import duckdb
import threading
import multiprocessing

from models import *
from utils import *
from logger.log import get_logger

log = get_logger('ingest_data')
processes = int(os.environ.get('PROCESSES_NO'))
ingest_batch_size = int(os.environ.get('INGEST_BATCH_SIZE'))

conn = duckdb.connect(database=os.environ.get('DUCKDB_PATH'), read_only=False)
conn.execute("""
    INSTALL postgres;
    LOAD postgres;
    ATTACH '' AS psql (TYPE POSTGRES);
""")

def load_data_in_batches(table_name, batch_size, progress, total):
    offset = 0
    while True:
        query = f"""
        CREATE OR REPLACE TABLE psql.{table_name} AS (
            SELECT *
            FROM {table_name}
            LIMIT {batch_size}
            OFFSET {offset}
        );
        """ if offset == 0 else f"""
        INSERT INTO psql.{table_name}
        SELECT *
        FROM {table_name}
        LIMIT {batch_size}
        OFFSET {offset};
        """
        conn.execute(query)
        rows_loaded = conn.execute(f"SELECT COUNT(*) FROM psql.{table_name}").fetchall().pop()[0]
        log.debug(f"Loaded {rows_loaded}/{total} rows into {table_name}")

        offset += batch_size
        progress.value += batch_size
        
        if rows_loaded >= total:
            break

if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        log.info("Starting data ingestion to PSQL...")
        files = find_files('./data/curated', 'json')
        batches = separate_files(files, os.environ.get('CURATED_REGEX'))

        total_records = 0
        for model in batches.keys():
            records = conn.execute(f"SELECT COUNT(*) FROM {model};").fetchall().pop()[0]
            batches[model] = records
            total_records += records
        
        progress_value = manager.Value('i', 0)
        progress_bar_process = multiprocessing.Process(target=create_progress_bar, args=(progress_value, total_records))
        progress_bar_process.start()
        
        print(batches)
        for model in batches.keys():
            log.info(f"Ingesting data for {model}...")
            load_data_in_batches(
                table_name = model,
                batch_size = ingest_batch_size,
                progress = progress_value,
                total = batches[model],
            )

        progress_bar_process.join()
        log.info("Ingestion to PSQL completed")