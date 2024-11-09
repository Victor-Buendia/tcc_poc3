import os
import json
import multiprocessing

from logger.log import get_logger
from models.BaseModel import faker
from utils import *
from models import *

log = get_logger('generate_data')
processes = int(os.environ.get('PROCESSES_NO'))
raw_path = os.environ.get('RAW_PATH')

def generate_data(process_id: int, model: BaseModel, record_amount: int, progress) -> None:
    try:
        faker.Faker.seed(process_id)
        model_name = model().__class__.__name__
        log.debug(f'Generating data for {model_name} in process {process_id}...')

        data = [model().__dict__ for _ in range(record_amount)]
        log.debug(f'Data successfully generated for {model_name} in process {process_id}...')

        log.debug(f'Saving data for {model_name} in process {process_id}...')

        with open(raw_path.format(model_name.lower(), model_name.lower(), process_id), 'w') as file:
            path = raw_path.format(model_name.lower(), model_name.lower(), process_id)
            log.debug(f'Saving data for for {model_name} in process {process_id} at {path}...')

            file.write(json.dumps(data))
            log.debug(f'Data successfully saved for {model_name} in process {process_id} at {path}...')

            progress.value += 1
            
    except Exception as e:
        log.error(e)

if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        log.info("Starting data generation...")

        log.info(f"{processes*len(models)} files will be generated")
        progress_value = manager.Value('i', 0)
        progress_bar_process = multiprocessing.Process(target=create_progress_bar, args=(progress_value, processes*len(models)))
        progress_bar_process.start()

        pool = multiprocessing.Pool()
        for model, records in models:
            log.info(f"Generating data for {model.__name__}...")
            for i in range(processes):
                pool.apply(
                    func = generate_data,
                    args = (i, model, records, progress_value),
                )
        pool.close()
        pool.join()
        progress_bar_process.join()
        log.debug("Data generation completed")