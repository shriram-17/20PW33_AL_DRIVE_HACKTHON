# GCS Folder Downloader

This Python script provides a multi-threaded and multi-process solution for downloading files from multiple Google Cloud Storage (GCS) folders to a local destination.

## Features

- Concurrent downloads using both multi-threading and multi-processing
- Handles multiple GCS folders
- Robust error handling
- Progress tracking and timing information

## Requirements

- Python 3.6+
- Google Cloud Storage Python Client Library

## Installation

1. Install the required library:
2. Ensure you have proper authentication set up for Google Cloud Storage.

## Usage

Run the script from the command line, providing one or more GCS folder URLs as arguments:
## Code Explanation

1. **Imports and Constants**:
   - The script uses the `google.cloud.storage` library for GCS operations.
   - `ThreadPoolExecutor` and `ProcessPoolExecutor` are used for concurrent execution.
   - `MAX_THREADS` and `MAX_PROCESSES` constants control the level of concurrency.

2. **download_file Function**:
   - Downloads a single file from GCS to the local destination.
   - Creates necessary directories if they don't exist.
   - Handles exceptions during download.

3. **download_files_from_bucket Function**:
   - Lists all blobs in a GCS bucket with a specific prefix.
   - Uses `ProcessPoolExecutor` to download files concurrently.

4. **process_gcs_folder Function**:
   - Processes a single GCS folder URL.
   - Extracts bucket name and source prefix from the URL.
   - Calls `download_files_from_bucket` to download files.
   - Measures and reports the time taken for each folder.

5. **main Function**:
   - Parses command-line arguments for GCS folder URLs.
   - Sets the destination directory.
   - Uses `ThreadPoolExecutor` to process multiple GCS folders concurrently.
   - Measures and reports the total time taken.

6. **Execution**:
   - The script is designed to be run as a standalone program.
   - It checks for command-line arguments and executes the main function.

## Logic and Thought Process

The script is designed with efficiency and scalability in mind, utilizing both multi-threading and multi-processing to optimize the download process from Google Cloud Storage. Here's a breakdown of the logic and thought process:

1. **Concurrency Model**:
   - The script uses a two-level concurrency model:
     a. Thread-level concurrency for handling multiple GCS folders
     b. Process-level concurrency for downloading files within each folder
   - This approach allows for efficient parallelization across both I/O-bound (network requests) and CPU-bound (file processing) tasks.

2. **Folder-Level Threading**:
   - Each GCS folder is processed in a separate thread using `ThreadPoolExecutor`.
   - This allows multiple folders to be downloaded simultaneously, improving overall throughput.
   - The number of concurrent folder processes is limited by `MAX_THREADS` to prevent overwhelming the system or network.

3. **File-Level Processing**:
   - Within each folder, file downloads are managed using `ProcessPoolExecutor`.
   - This leverages multiple CPU cores for parallel downloads and file writing operations.
   - The `MAX_PROCESSES` constant controls the number of concurrent file downloads per folder.

4. **Error Handling and Robustness**:
   - Each file download is wrapped in a try-except block to handle individual failures gracefully.
   - Errors are reported but do not halt the entire process, ensuring maximum data retrieval even if some files fail.

5. **Performance Monitoring**:
   - The script measures and reports the time taken for each folder and the total execution time.
   - This provides valuable insights into performance across different scenarios (e.g., large files vs. many small files).

6. **Flexibility and Ease of Use**:
   - The script accepts multiple GCS folder URLs as command-line arguments, allowing for flexible batch processing.
   - It automatically creates necessary local directories, simplifying the download process.

7. **Resource Management**:
   - By using `ThreadPoolExecutor` and `ProcessPoolExecutor`, the script efficiently manages system resources.
   - These executors handle the creation and cleanup of threads and processes, preventing resource leaks.

8. **Scalability Considerations**:
   - The `MAX_THREADS` and `MAX_PROCESSES` constants can be adjusted based on the system's capabilities and network conditions.
   - This allows the script to be fine-tuned for different environments, from personal computers to high-performance servers.

9. **Modular Design**:
   - The code is structured into distinct functions (`download_file`, `download_files_from_bucket`, `process_gcs_folder`), each with a specific responsibility.
   - This modular approach enhances readability, maintainability, and potential for future enhancements.

The overall design aims to balance speed, efficiency, and reliability, making it suitable for downloading large amounts of data from GCS in various scenarios, from a few large files to many small files.

## Performance Considerations

- Adjust `MAX_THREADS` and `MAX_PROCESSES` based on your system's capabilities and network conditions.
- The script uses multi-processing for file downloads within each folder and multi-threading for processing multiple folders.

## Error Handling

- The script includes try-except blocks to handle exceptions during file downloads and folder processing.
- Failed downloads are reported but do not halt the entire process.

## Output

- The script prints progress information, including time taken for each folder and the total execution time.

## Benchmark Results

Here are the updated benchmark results for different scenarios:

* gs://ai-drive-psg-2024-us-central1/scenario_2_medium_files/ => 32.34 seconds
* gs://ai-drive-psg-2024-us-central1/scenario_3_small_files/ => 56.90 seconds
* gs://ai-drive-psg-2024-us-central1/scenario_1_large_file/ => 83.39 seconds
* gs://ai-drive-psg-2024-us-central1/scenario_4_very_small_files/ => 135.62 seconds

Total execution time: 3 minutes and 8.62 seconds

System resource usage:
* real time: 3m8.829s
* user time: 6m56.127s
* sys time: 4m13.477s

These benchmarks demonstrate the script's performance across different file size scenarios, from large files to very small files. The script handles medium-sized files most efficiently in this case, while scenarios with many very small files take the longest due to the overhead of initiating multiple downloads.

The total execution time is less than the sum of individual scenario times, indicating effective parallel processing. The user and sys times being higher than the real time further confirms the script's utilization of multiple cores/threads for concurrent operations.

## Note

Ensure you have the necessary permissions to access the specified GCS buckets and write to the destination directory.