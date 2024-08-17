from typing import Generator, List
import os
from linetimer import CodeTimer
from tqdm import tqdm
def scandir_yield_files(directory):
    """Generator that yields file paths in a directory."""
    with os.scandir(directory) as it:
        for entry in it:
            if entry.is_file():
                yield entry.path

def path_generator(directory: str, batch_size: int = 100) -> Generator[List[str], None, None]:
    batch = []
    for path in scandir_yield_files(directory):
        batch.append(path)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

my_path = "/mnt/q/logs/2024-07-15_RC24/2024-07-20_11-15-00_BerlinUnited_vs_HTWK_half2/extracted/3_22_Nao0004_240720-1206/log_bottom_jpg"
num = os.system(f"ls -f {my_path} | wc -l")
print(num)
quit()
with CodeTimer():
    for batch in path_generator(my_path):
        for idx, file in tqdm(enumerate(batch)):
            #with CodeTimer('loop 1'):
            pass