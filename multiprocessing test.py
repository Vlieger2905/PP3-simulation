import multiprocessing
import time

def process_chunk(chunk):
    # Simulate some processing by squaring the numbers in the chunk
    return [n * n for n in chunk]

def main():
    numbers = list(range(1, 1000000001))  # A list of 1,000 numbers
    chunk_size = 100  # Size of each chunk
    num_chunks = len(numbers) // chunk_size  # Number of chunks

    # Create a pool of workers
    with multiprocessing.Pool(processes=4) as pool:
        results = []
        for i in range(num_chunks):
            chunk = numbers[i * chunk_size:(i + 1) * chunk_size]
            result = pool.apply_async(process_chunk, (chunk,))
            results.append(result)

        # Collect the results
        squared_numbers = []
        for result in results:
            squared_numbers.extend(result.get())

    print(f"Original numbers: {numbers[:10]} ... {numbers[-10:]}")  # Show a slice for brevity
    print(f"Squared numbers: {squared_numbers[:10]} ... {squared_numbers[-10:]}")  # Show a slice for brevity

if __name__ == "__main__":
    main()
