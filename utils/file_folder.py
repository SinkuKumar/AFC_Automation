import os
import time
import shutil
import logging
from datetime import datetime

class FileOperations:
    """
    Perform file operations such as creating directories, clearing directory contents, and moving files.
    """

    def __init__(self) -> None:
        pass

    def create_directories(self, paths: list[str]) -> None:
        """
        Create one or more directories if they do not already exist.

        This method takes a list of directory paths and attempts to create each directory.

        Args:
            paths (list[str]): A list of directory paths to be created.

        Returns:
            None

        Raises:
            PermissionError: If the script lacks permissions to create a directory.
            OSError: For general OS-related errors during file operations.
            Exception: Catches any unforeseen exceptions that may occur.
        """
        for path in paths:
            try:
                if not os.path.exists(path):
                    os.makedirs(path, exist_ok=True)
                    logging.info(f"Directory created successfully: {path}")
                else:
                    logging.info(f"Directory already exists: {path}")
            except PermissionError:
                logging.error(f"Permission denied: Unable to create directory '{path}'.")
            except OSError as e:
                logging.error(f"OS error occurred while creating directory '{path}': {e}")
            except Exception as e:
                logging.critical(f"Unexpected error while creating directory '{path}': {e}", exc_info=True)

    def clear_directory_files(self, directory_path: str) -> None:
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

    def wait_for_download(self, report_name: str, download_directory: str, timeout: int = 300, sleep_interval: int = 1) -> None:
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

    def move_file(file_path, base_directory, client_id=None):
        """
        Moves a file into a subfolder named with the current date inside the given base directory.
        Optionally, the file can be renamed to include the client ID before the file extension.

        Process:
            - Creates a folder named with the current date (format: YYYY_MM_DD) inside `base_directory`.
            - Moves `file_path` into this folder.
            - If `client_id` is provided, appends `_clientid` to the filename before the extension.

        Args:
            file_path (str): full path of the file to be moved.
            base_directory (str): path to the base directory where the dated folder should be created.
            client_id (str, optional (default=None)): optional client ID to append to the file name before the file extension.

        Returns:
            None

        Raises:
            Exception if the file move operation fails.

        Example:
            file_path = '/path/to/data.csv'
            base_directory = '/new/location'
            client_id = '12345'

            It will be moved to:
                /new/location/2025_02_28/data_12345.csv

            If `client_id` is not provided:
                /new/location/2025_02_28/data.csv
        """
        today_date = datetime.today().strftime("%Y_%m_%d")

        folder_path = os.path.join(base_directory, today_date)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logging.info(f"Directory '{folder_path}' created successfully.")
        else:
            logging.info(f"Directory '{folder_path}' already exists.")

        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)

        if client_id:
            new_file_name = f"{name}_{client_id}{ext}"
        else:
            new_file_name = file_name

        new_file_path = os.path.join(folder_path, new_file_name)

        try:
            shutil.move(file_path, new_file_path)
            logging.info(f"File '{file_name}' moved to '{new_file_path}' successfully.")
        except Exception as e:
            logging.error(f"An error occurred while moving the file '{file_path}' to '{new_file_path}': {e}")
            raise
