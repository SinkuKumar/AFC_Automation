.. _using_automation:

Using Automation
================

To use the automation script, follow these steps:

1. **Create a Python File:**
   - In the root directory of the project, create a new Python file, such as ``mtd_uploads.py``.
   - This file can be reused with different client IDs.

2. **Add the Following Code:**

   .. code-block:: python

      from download_reports import execute_report_functions
      from utils.report_date import get_past_date
      from utils.etl.report_config import CURRENT_DATE

      client_id = 3622
      mode = "include"
      report_list = ["CNT_27"]

      report_config = {
          "CNT_27": {"from_date": get_past_date(days=60), "to_date": CURRENT_DATE},
      }

      execute_report_functions(client_id, mode, report_list, function_args=report_config)

3. **Run the Script:** Execute the Python file using the following command:

   .. code-block:: bash

      python mtd_uploads.py

4. **Check the Output:** The downloaded files will be saved in the ``downloads`` directory of the root project folder. The data will be inserted into the ``CNT_27_Staging_3622`` database.
