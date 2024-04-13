from milestone_tagger import handle_input_milestone
from yaml_parse import load, evaluate

milestones = load("proto_milestones_dev.yml")
input_milestone = milestones[0]
compound_or_milestone = milestones[1]
compound_and_milestone = milestones[8]
output_milestone = milestones[4]

for i, m in enumerate(milestones):
    if m.label == "compound":
        print(f"{i} {m}")
print("input milestone: ", input_milestone)
print("output milestone: ", output_milestone)
print("compound milestone: ", compound_or_milestone)


def test_evaluate_input():
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

    input_milestone.value = "ssh 10.12.0.7 -p 123"

    assert evaluate(input_milestone, csv_line)
    assert not evaluate(input_milestone, bad_csv_line)


def test_evaluate_output():
    # modified output line to pass, I believe
    csv_line = {
        "hostname": "FirstStop",
        "timestamp": "1705265538",
        "directory": "/home/devuser3",
        "stdin": "some command",
        "output": "some random output 7035efa5",
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

    assert evaluate(output_milestone, csv_line)
    assert not evaluate(output_milestone, bad_csv_line)


def test_evaluate_or():
    compound_or_milestone.right.value = "10.12.0.13"
    print("left: ", compound_or_milestone.left)
    print("right: ", compound_or_milestone.right)
    csv_line = {
        "hostname": "FirstStop",
        "timestamp": "1705265538",
        "directory": "/home/devuser3",
        "stdin": "some command",
        "output": "some random output 7035efa5",
        "prompt": "devuser3@FirstStop:~",
    }

    # both false
    assert not evaluate(compound_or_milestone, csv_line)

    # left true
    tmp_csv_line = csv_line.copy()
    tmp_csv_line["stdin"] = "nmap 10.12.0.0"
    print(tmp_csv_line)
    assert evaluate(compound_or_milestone, tmp_csv_line)

    # right true
    tmp_csv_line = csv_line.copy()
    tmp_csv_line["output"] = "Starting Nmap... \n10.12.0.13"
    print(tmp_csv_line)
    assert evaluate(compound_or_milestone, tmp_csv_line)

    # both true
    csv_line["stdin"] = "nmap 10.12.0.0"
    csv_line["output"] = "StartingNma... \n10.12.0.13"
    print(csv_line)
    assert evaluate(compound_or_milestone, csv_line)


def test_evaluate_and():
    print(compound_and_milestone)
    print("left: ", compound_and_milestone.left)
    print("right: ", compound_and_milestone.right)
    csv_line = {
        "hostname": "FirstStop",
        "timestamp": "1705265538",
        "directory": "/home/devuser3",
        "stdin": "some command",
        "output": "some random output 7035efa5",
        "prompt": "devuser3@FirstStop:~",
    }

    # both false
    assert not evaluate(compound_and_milestone, csv_line)

    # left true
    tmp_csv_line = csv_line.copy()
    tmp_csv_line["stdin"] = "base64 --decode -d betcha_cant_read_me"
    assert evaluate(compound_and_milestone.left, tmp_csv_line)
    assert not evaluate(compound_and_milestone, tmp_csv_line)

    # right true
    tmp_csv_line = csv_line.copy()
    tmp_csv_line["output"] = "You found me. Good job."
    assert evaluate(compound_and_milestone.right, tmp_csv_line)
    assert not evaluate(compound_and_milestone, tmp_csv_line)

    # both true
    csv_line["stdin"] = "base64 --decode -d betcha_cant_read_me"
    csv_line["output"] = "You found me. Good job."
    assert evaluate(compound_and_milestone, csv_line)
