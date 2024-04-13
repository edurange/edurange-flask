import yaml
from milestone_tagger import (
    handle_input_milestone,
    handle_output_milestone,
    handle_compound_milestone,
)

with open("proto_milestones_dev.yml", "r") as yml:
    document = yaml.full_load(yml)
    milestones = document[0]["Milestones"]["Prototype"]


def test_input():
    input_milestones = [x for x in milestones if x["Type"] == "Input"]
    csv_line = {
        "hostname": "NAT",
        "timestamp": "1705265502",
        "directory": "/home/devuser3",
        "stdin": "ssh 10.12.0.7 -p 123",
        "output": "\nThe authenticity of host '[10.12.0.7]:123 ([10.12.0.7]:123)' can't be established.\nECDSA key fingerprint is SHA256:4utoWe5uVp79ImYqkPPukjmrGIfvDC5demc1sx8sY9c.\nAre you sure you want to continue connecting (yes/no)? yes\nWarning: Permanently added '[10.12.0.7]:123' (ECDSA) to the list of known hosts.\ndevuser3@10.12.0.7's password: \n ███████╗██╗██████╗ ███████╗████████╗    ███████╗████████╗ ██████╗ ██████╗\n ██╔════╝██║██╔══██╗██╔════╝╚══██╔══╝    ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗\n █████╗  ██║████",
        "prompt": "devuser3@NAT:~",
    }
    bad_csv_line = {
        "hostname": "NAT",
        "timestamp": "1705265502",
        "directory": "/home/devuser3",
        "stdin": "ssh 10.12.0.7",
        "output": "\nThe authenticity of host '[10.12.0.7]:123 ([10.12.0.7]:123)' can't be established.\nECDSA key fingerprint is SHA256:4utoWe5uVp79ImYqkPPukjmrGIfvDC5demc1sx8sY9c.\nAre you sure you want to continue connecting (yes/no)? yes\nWarning: Permanently added '[10.12.0.7]:123' (ECDSA) to the list of known hosts.\ndevuser3@10.12.0.7's password: \n ███████╗██╗██████╗ ███████╗████████╗    ███████╗████████╗ ██████╗ ██████╗\n ██╔════╝██║██╔══██╗██╔════╝╚══██╔══╝    ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗\n █████╗  ██║████",
        "prompt": "devuser3@NAT:~",
    }
    assert handle_input_milestone(input_milestones[0], csv_line)
    assert not handle_input_milestone(input_milestones[0], bad_csv_line)


def test_output():
    output_milestones = [x for x in milestones if x["Type"] == "Output"]
    # modified output line to pass, I believe
    csv_line = {
        "hostname": "FirstStop",
        "timestamp": "1705265538",
        "directory": "/home/devuser3",
        "stdin": "nmap 10.12.0.0/27",
        "output": "\n\nStarting Nmap 7.01 10.12.0.13",
        "prompt": "devuser3@FirstStop:~",
    }
    bad_csv_line = {
        "hostname": "FirstStop",
        "timestamp": "1705265538",
        "directory": "/home/devuser3",
        "stdin": "nmap 10.12.0.0/27",
        "output": "\n\nStarting Nmap 7.01 ",
        "prompt": "devuser3@FirstStop:~",
    }
    assert handle_output_milestone(output_milestones[0], csv_line)
    assert not handle_output_milestone(output_milestones[0], bad_csv_line)


def test_compound():
    compound_milestones = [x for x in milestones if x["Type"] == "Compound"]
    bitvector = {ms["Label"]: 0 for ms in milestones}
    bitvector["M2"] = 1
    bitvector["M3"] = 1
    assert handle_compound_milestone(compound_milestones[0], bitvector)
    bitvector["M2"] = 0
    assert not handle_compound_milestone(compound_milestones[0], bitvector)
    bitvector["M3"] = 0
    assert not handle_compound_milestone(compound_milestones[0], bitvector)
    
