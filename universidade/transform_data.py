import os
import multiprocessing

from logger.log import get_logger
from models import *
from utils import *
from transform import *

log = get_logger("transform_data")
processes = int(os.environ.get("PROCESSES_NO"))


def transform_data(thread_id: int, dir_name: str, file_path: str, process) -> None:
    log.debug(f"Transforming {dir_name} {file_path} {thread_id}")

    transformation_mapping[dir_name](dir_name, file_path, thread_id)
    log.debug(f"Completed transforming for {dir_name} {file_path} {thread_id}")

    process.value += 1


if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        log.info("Starting data transformation...")

        files = find_files("./data/raw", "json")
        log.info(f"Found {len(files)} files to process")
        log.debug(f"Files found: {files}")

        log.info(f"{len(files)} files will be transformed")
        progress_value = manager.Value("i", 0)
        progress_bar_process = multiprocessing.Process(
            target=create_progress_bar, args=(progress_value, len(files))
        )
        progress_bar_process.start()

        batches = separate_files(files, os.environ.get("RAW_REGEX"))
        log.info(
            f"The files were separated in {len(batches)} batches, namely: {list(batches.keys())}"
        )
        log.debug(f"Files in each batch: {batches}")

        pool = multiprocessing.Pool()
        for dir_name in batches.keys():
            log.info(f"Transforming data for {dir_name}...")
            [
                pool.apply(
                    func=transform_data,
                    args=(i, dir_name, batches[dir_name][i], progress_value),
                )
                for i in range(len(batches[dir_name]))
            ]
        pool.close()
        pool.join()
        progress_bar_process.join()
        log.info("Transformation completed")
