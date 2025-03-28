.. _installation:

Installation
============

Download or clone the repository:

.. code-block:: bash

   git clone https://github.com/SinkuKumar/AFC_Automation.git

In the source code directory, create a file named ``.env`` with the following credentials:

.. code-block:: ini

   SMTP_ADDRESS = 'smtp.office365.com'
   SMTP_PORT = '587'
   SMTP_ACCOUNT = 'user@domain.com'
   SMTP_PASSWORD = 'secret-password'
   SQL_SERVER = '127.0.0.1'
   SQL_DATABASE = 'BI_AFC_Experity'
   SQL_USERNAME = 'username'
   SQL_PASSWORD = 'password'

Update the contents of the ``.env`` file as per your configuration. Now, the automation scripts are ready to use.

Create and Activate Virtual Environment
----------------------------------------

For macOS/Linux:

.. code-block:: bash

   python3 -m venv venv
   source venv/bin/activate

For Windows:

.. code-block:: powershell

   python -m venv venv
   venv\Scripts\activate

.. warning::
   In a production environment, do not create a new virtual environment or activate it. Use the system-installed configuration for best results.

Install Dependencies
---------------------

Run the following command to install the required dependencies:

.. code-block:: bash

   pip install -r requirements.txt
