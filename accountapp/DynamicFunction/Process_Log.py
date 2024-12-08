import requests
def ProcessLogFunction(process_id, log_date, log_output_file, log_data_type, log_process_name, error):
    # API_PROCESS_LOG = "http://127.0.0.1:8000/account/process-log/"
    API_PROCESS_LOG = "https://itb-usa.a2hosted.com/account/process-log/"
    process_data = [{
        'process_id': process_id,
        "log_date": log_date,
        "log_output_file": log_output_file,
        "log_data_type": log_data_type,
        "log_process_name": log_process_name,
        "log_error": error,
    }]
    r = requests.post(url=API_PROCESS_LOG, json=process_data)
    print("14", r.text)
    
def InternalProcessLogFunction(process_id, log_date, status_code, message):
    # API_PROCESS_LOG = "http://127.0.0.1:8000/account/internal-process-log/"
    API_INTERNAL_PROCESS_LOG = "https://itb-usa.a2hosted.com/account/internal-process-log/"
    internal_process_data = [{
        "process_id": process_id,
        "log_date": log_date,
        "status_code": status_code,
        "message": message
    }]
    r = requests.post(url=API_INTERNAL_PROCESS_LOG, json=internal_process_data)
    print("14", r.text)
    
    
def HeartBeatFunction(response_time, server_name, status):
    HeartBeat_LOG = "https://itb-usa.a2hosted.com/account/heartbeat/"
    heartbeat_data = [{
        "response_time": response_time,
        "server_name": server_name,
        "status": status
    }]
    r = requests.post(url=HeartBeat_LOG, json=heartbeat_data)
    print("14", r.text)

