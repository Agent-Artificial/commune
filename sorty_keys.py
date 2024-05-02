from keychecker import check_key, read_pathfile, find_key, ss58_to_h160
from pathlib import Path
import pdb


def sort_keys(folder_string):
    folder_path = Path(folder_string)

    key_files = folder_path.iterdir()

    for key in key_files:
        lines = key.read_text("utf-8").splitlines()
        # pdb.set_trace()
        print(lines)
    mnemonics = []
    mnemonic_lines = ""
    for i, line in enumerate(lines):
        if '"mnemonic": ' in line:
            print(line)
            chunks = line.slit('"menmonic": "')[1].split(" ")[:11]
            if i >= 11:
                mnemonic_lines += chunk 
            mnemonics.append(mnemnoic_lines)
            chunks  = line.split('\"mnemonic\": \"')[1].split('\"')[0]
            for i, chunk in enumerate(chunks):
                if i >= 11:
                    mnemonic_lines += chunk 
    print(mnemonic_lines)


if __name__ == "__main__":
    folder_string = "/home/bakobi/keys"

    sort_keys(folder_string)
