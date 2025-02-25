import os
import time
import logging

def clear_directory_files(directory_path: str) -> None:
    """
    Deletes all files in the specified directory without affecting subdirectories.

    Args:
        directory_path (str): The absolute or relative path of the directory whose files need to be cleared.

    Returns:
        None

    Raises:
        ValueError: If the provided directory path does not exist or is not a directory.
        PermissionError: If the script lacks permissions to read or modify the directory or files.
        FileNotFoundError: If a file is not found during deletion (possibly already deleted).
        OSError: For general OS-related errors during file operations.
        Exception: Catches any unforeseen exceptions that may occur.
    """
    if not os.path.exists(directory_path):
        logging.error(f"Provided directory does not exist: {directory_path}")
        raise ValueError(f"Directory does not exist: {directory_path}")

    if not os.path.isdir(directory_path):
        logging.error(f"Provided path is not a directory: {directory_path}")
        raise ValueError(f"Path is not a directory: {directory_path}")

    logging.info(f"Starting to clear files in directory: {directory_path}")

    try:
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                try:
                    os.unlink(file_path)
                    logging.info(f"Deleted file: {file_path}")
                except PermissionError:
                    logging.error(f"Permission denied to delete file: {file_path}")
                    raise
                except FileNotFoundError:
                    logging.warning(f"File not found (might have been deleted already): {file_path}")
                    raise
                except OSError as e:
                    logging.error(f"OS error while deleting file {file_path}: {e}")
                    raise

        logging.info(f"Completed clearing files in directory: {directory_path}")

    except PermissionError:
        logging.error(f"Permission denied to access directory: {directory_path}")
        raise
    except OSError as e:
        logging.error(f"OS error while accessing directory {directory_path}: {e}")
        raise
    except Exception as e:
        logging.critical(f"Unexpected error occurred: {e}", exc_info=True)
        raise

def wait_for_download(report_name: str, download_directory: str, timeout: int = 300, sleep_interval: int = 1) -> None:
    """
    Waits for a file download to complete in the specified directory.

    This function continuously monitors the download directory for a file that starts with 
    the given `report_name` and ensures it is fully downloaded (i.e., no temporary extensions 
    like `.part` or `.crdownload`).

    Args:
        report_name (str): The expected prefix of the downloaded file.
        download_directory (str): The directory where the file is expected to be downloaded.
        timeout (Optional[int]): Maximum time (in seconds) to wait before giving up. Default is 300 seconds.
        sleep_interval (Optional[int]): Interval (in seconds) between directory checks. Default is 1 second.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified download directory does not exist.
        TimeoutError: If the download does not complete within the specified timeout.
        PermissionError: If the script lacks permissions to read the download directory.
        Exception: Catches unforeseen exceptions and logs detailed error info.
    """
    start_time = time.time()

    if not os.path.exists(download_directory):
        logging.error(f"Download directory does not exist: {download_directory}")
        raise FileNotFoundError(f"Download directory not found: {download_directory}")

    if not os.path.isdir(download_directory):
        logging.error(f"Provided path is not a directory: {download_directory}")
        raise ValueError(f"Path is not a directory: {download_directory}")

    logging.info("Waiting for download to start...")

    try:
        # Wait for the download to start
        while not any(file.startswith(report_name) for file in os.listdir(download_directory)):
            if time.time() - start_time > timeout:
                logging.error("Download did not start within the timeout period.")
                raise TimeoutError("Download did not start within the allowed time.")
            time.sleep(sleep_interval)

        logging.info("Download started...")

        # Wait for the partial download to complete
        while any(file.endswith((".part", ".crdownload")) for file in os.listdir(download_directory)):
            if time.time() - start_time > timeout:
                logging.error("Partial file is still present after timeout.")
                raise TimeoutError("Download stuck in partial state.")
            time.sleep(sleep_interval)

        logging.info("Partial download completed.")

        # Confirm the final file is available
        while not any(file.startswith(report_name) and file.endswith((".csv", ".xlsx", ".txt")) for file in os.listdir(download_directory)):
            if time.time() - start_time > timeout:
                logging.error("Final file not found after timeout.")
                raise TimeoutError("Final file was not detected after the allowed time.")
            time.sleep(sleep_interval)

        time.sleep(2)  # Final small wait to ensure file is stable
        logging.info("File download completed successfully.")

    except PermissionError:
        logging.error("Permission denied while accessing the download directory.")
        raise

    except TimeoutError as te:
        logging.error(f"TimeoutError: {te}")
        raise

    except Exception as e:
        logging.critical(f"Unexpected error occurred: {e}", exc_info=True)
        raise
