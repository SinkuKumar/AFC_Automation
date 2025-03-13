import subprocess

# List of client IDs to process
client_ids = ['16', '3622', '3630', '3735', '3625', '3649', '3650', '3736', '822', '655', '3657', '640', '489', '36', '3671', '3672', '3624', '3678', '3681', '3696', '3698', '3697', '3705', '3716', '3720', '3718', '3665', '3724', '3725', '3726', '3670']  # Add more client IDs as needed

for client_id in client_ids:
    print(f"Processing client ID: {client_id}")
    subprocess.run(["python", "import_clinic_data.py", client_id])
    print(f"Completed client ID: {client_id}\n")
