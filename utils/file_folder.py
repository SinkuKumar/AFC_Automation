import os
import time
import shutil
import logging
from datetime import datetime

def create_directories(paths: list[str]) -> None:
    """
    Create one or more directories if they do not already exist.
    This method takes a list of directory paths and attempts to create each directory.

    :param paths: A list of directory paths to be created.
    :type paths: list[str]

    :returns: None

    :raises PermissionError: If the script lacks permissions to create a directory.
    :raises OSError: For general OS-related errors during file operations.
    :raises Exception: Catches any unforeseen exceptions that may occur.
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
            raise
        except OSError as e:
            logging.error(f"OS error occurred while creating directory '{path}': {e}")
            raise
        except Exception as e:
            logging.critical(f"Unexpected error while creating directory '{path}': {e}", exc_info=True)
            raise

def clear_directory_files(directory_path: str) -> None:
    """
    Deletes all files in the specified directory without affecting subdirectories.

    :param directory_path: The absolute or relative path of the directory whose files need to be cleared.
    :type directory_path: str

    :returns: None

    :raises ValueError: If the provided directory path does not exist or is not a directory.
    :raises PermissionError: If the script lacks permissions to read or modify the directory or files.
    :raises FileNotFoundError: If a file is not found during deletion (possibly already deleted).
    :raises OSError: For general OS-related errors during file operations.
    :raises Exception: Catches any unforeseen exceptions that may occur.
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

def init_directory(directory_path: str) -> None:
    """
    Creates a directory if it does not already exist.
    Clear all the files in the directory if it already exists.

    :param directory_path: The absolute or relative path of the directory which is to be initialized.
    :type directory_path: str
    """
    if os.path.exists(directory_path):
        clear_directory_files(directory_path)
    else:
        create_directories([directory_path])

def wait_for_download(report_name: str, download_directory: str, timeout: int = 300, sleep_interval: int = 1) -> None:
    """
    Waits for a file download to complete in the specified directory.

    This function continuously monitors the download directory for a file that starts with 
    the given `report_name` and ensures it is fully downloaded (i.e., no temporary extensions 
    like `.part` or `.crdownload`).

    :param report_name: The expected prefix of the downloaded file.
    :type report_name: str
    :param download_directory: The directory where the file is expected to be downloaded.
    :type download_directory: str
    :param timeout: Maximum time (in seconds) to wait before giving up. Default is 300 seconds.
    :type timeout: int, optional
    :param sleep_interval: Interval (in seconds) between directory checks. Default is 1 second.
    :type sleep_interval: str, optional

    :returns: None

    :raises FileNotFoundError: If the specified download directory does not exist.
    :raises TimeoutError: If the download does not complete within the specified timeout.
    :raises PermissionError: If the script lacks permissions to read the download directory.
    :raises Exception: Catches unforeseen exceptions and logs detailed error info.
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
        return os.path.join(download_directory, [file for file in os.listdir(download_directory) if file.startswith(report_name)][0])

    except PermissionError:
        logging.error("Permission denied while accessing the download directory.")
        raise

    except TimeoutError as te:
        logging.error(f"TimeoutError: {te}")
        raise

    except Exception as e:
        logging.critical(f"Unexpected error occurred: {e}", exc_info=True)
        raise

def rename_file_or_folder(old_name: str, new_name: str) -> None:
    """
    Renames a file or folder from `old_name` to `new_name`.

    :param old_name: The current name (or path) of the file or folder.
    :type old_name: str
    :param new_name: The new name (or path) to rename the file or folder.
    :type new_name: str
    :returns: True if renaming was successful, False otherwise.
    :rtype: bool

    :raises FileNotFoundError: If the specified `old_name` does not exist.
    :raises FileExistsError: If a file or folder with `new_name` already exists.
    :raises PermissionError: If the operation is not permitted due to system restrictions.
    :raises OSError: For other OS-related errors.
    """
    try:
        if not os.path.exists(old_name):
            raise FileNotFoundError(f"Error: '{old_name}' does not exist.")

        if os.path.exists(new_name):
            raise FileExistsError(f"Error: A file or folder named '{new_name}' already exists.")

        os.rename(old_name, new_name)
        logging.info(f"Successfully renamed '{old_name}' to '{new_name}'.")

    except (FileNotFoundError, FileExistsError, PermissionError, OSError) as e:
        logging.error(f"Failed to rename from {old_name} to {new_name}.")
        raise

def move_paths(sources: list[str], destination: str) -> None:
    """
    Moves multiple files or folders from the source paths to the destination path.

    If the destination is an existing directory, each source will be moved inside it. 
    If the destination path does not exist, it will be created.

    :param sources: A list of file or directory paths to move.
    :type sources: List[str]
    :param destination: The target directory where files/folders should be moved.
    :type destination: str

    :raises FileNotFoundError: If any source file or directory does not exist.
    :raises PermissionError: If the process lacks the necessary permissions.
    :raises Exception: If any other unexpected error occurs during the move operation.
    """
    try:
        if not isinstance(sources, list) or not sources:
            raise ValueError("Sources must be a non-empty list of file/folder paths.")

        if not os.path.exists(destination):
            os.makedirs(destination, exist_ok=True)  # Create destination if not exists

        for source in sources:
            if not os.path.exists(source):
                logging.warning(f"Skipping: Source path does not exist: {source}")
                continue

            if os.path.isdir(destination):  
                shutil.move(source, os.path.join(destination, os.path.basename(source)))
            else:
                shutil.move(source, destination)

            logging.info(f"Successfully moved '{source}' to '{destination}'")

    except FileNotFoundError as e:
        logging.error(f"Error: {e}")
        raise
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def move_files_only(source_folder: str, destination_folder: str) -> None:
    """
    Moves all files (but not subfolders) from the source folder to the destination folder.

    :param source_folder: The folder containing files to be moved.
    :type source_folder: str
    :param destination_folder: The folder where the files should be moved.
    :type destination_folder: str

    :raises FileNotFoundError: If the source folder does not exist.
    :raises PermissionError: If the process lacks necessary permissions.
    :raises Exception: If any other unexpected error occurs.
    """
    try:
        if not os.path.exists(source_folder):
            raise FileNotFoundError(f"Source folder does not exist: {source_folder}")

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for item in os.listdir(source_folder):
            source_path = os.path.join(source_folder, item)
            destination_path = os.path.join(destination_folder, item)

            if os.path.isfile(source_path):
                shutil.move(source_path, destination_path)
                logging.info(f"Moved files form Temporary folder to All files folder")

        logging.info("All files have been moved successfully.")

    except FileNotFoundError as e:
        logging.error(f"Error: {e}")
        raise
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def move_file(src_path: str, dest_dir:str) -> None:
    """
    Move a file from the source path to the destination directory.

    :param src_path: The path of the file to be moved.
    :type src_path: str
    :param dest_dir: The directory where the file should be moved.
    :type dest_dir: str
    :returns: None

    :raises FileNotFoundError: If the source file does not exist.
    :raises PermissionError: If the process lacks necessary permissions.
    :raises Exception: If any other unexpected error occurs.
    """
    try:
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source file does not exist: {src_path}")

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        shutil.move(src_path, dest_dir)
        logging.info(f"File moved from {src_path} to {dest_dir}")

    except FileNotFoundError as e:
        logging.error(f"Error: {e}")
        raise
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def move_items(sources: str | list[str], destination: str, files_only: bool = False) -> None:
    """
    Moves files or folders from the source(s) to the destination.

    :param sources: A single path or a list of paths to move.
    :type sources: str | list[str]
    :param destination: The target directory.
    :type destination: str
    :param files_only: If True, only files from a folder are moved (subfolders are ignored). Defaults to False.
    :type files_only:  Optional[bool]

    :raises FileNotFoundError: If a source file or folder does not exist.
    :raises PermissionError: If there is an issue with file permissions.
    :raises Exception: For any unexpected errors.
    """

    if isinstance(sources, str):
        sources = [sources]

    try:
        if not os.path.exists(destination):
            os.makedirs(destination, exist_ok=True)
            logging.info(f"Created destination directory: {destination}")

        for src in sources:
            if not os.path.exists(src):
                logging.error(f"Source not found: {src}")
                raise FileNotFoundError(f"Source not found: {src}")

            if os.path.isdir(src) and files_only:
                for item in os.listdir(src):
                    src_item = os.path.join(src, item)
                    if os.path.isfile(src_item):
                        shutil.move(src_item, os.path.join(destination, item))
                        logging.info(f"Moved file: {src_item} -> {destination}")
            else:
                shutil.move(src, destination)
                logging.info(f"Moved: {src} -> {destination}")

    except FileNotFoundError as e:
        logging.error(f"File not found error: {e}")
        raise
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

def delete_directories(directories: str | list[str]) -> None:
    """Delete one or multiple directories safely without confirmation.

    :param directories: A single directory path or a list of directory paths to delete.
    :type directories: str | list[str]
    :returns: None

    :raises ValueError: If `directories` is not a string or list.
    :raises PermissionError: If the directory cannot be deleted due to permissions.
    :raises OSError: If an unexpected OS error occurs.
    """
    if isinstance(directories, str):
        directories = [directories]
    elif not isinstance(directories, list):
        raise ValueError("Expected a string or list of strings for directories.")

    for directory in directories:
        try:
            if not os.path.exists(directory):
                logging.warning(f"Directory '{directory}' does not exist.")
                continue

            shutil.rmtree(directory)
            logging.info(f"Successfully deleted directory: {directory}")

        except PermissionError:
            logging.error(f"Permission denied: Cannot delete '{directory}'.")
            raise
        except OSError as e:
            logging.error(f"OS error occurred while deleting '{directory}': {e}")
            raise