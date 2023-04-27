import requests
import json
import sys
import subprocess

project_root_directory = "/Users/olympixengineering/aa-code/smart-contracts-testing" # the root of your project, where your hardhat.config or foundry.toml is
hardhat_flatten_cmd = ["npx", "hardhat", "flatten"]
foundry_flatten_cmd =  ["forge", "flatten"]

# switch flattening command based on if you are using hardhat or foundry 
framework_flatten_cmd = foundry_flatten_cmd

# set to https://olympixdevsectools.com/ for prod
olympix_api = "https://olympixdevsectools.com/"
missing_checks_endpoint = olympix_api + "solmischecks"

relative_path_to_solidity = sys.argv[1] # path from project root to solidity file we want to analyze
flatten_cmd = framework_flatten_cmd + [relative_path_to_solidity]

tmp_file_path = "tmp.sol" # we need a temp file because the flattened code might be too long for stdout. You can configure this tmp file to be where you'd like
with open(tmp_file_path, "w") as output_file:
    process = subprocess.Popen(flatten_cmd, cwd=project_root_directory, stdout=output_file, stderr=subprocess.STDOUT)
    process.wait()
    
tmp_file_readable = open(tmp_file_path, "r")
flat_sol = tmp_file_readable.read()
tmp_file_readable.close()

flat_sol = flat_sol.replace("SPDX", "////") # this is neccessary because solc won't compile a file with more than one SPDX lisence

examine_sol_file = open("/Users/olympixengineering/aa-code/smart-contracts-testing/StablecoinBridge.sol", "w")
examine_sol_file.write(flat_sol)
examine_sol_file.close()


# flat_sol = flat_sol.replace("SPDX", "////") # this is neccessary because solc won't compile a file with more than one SPDX lisence

# payload = json.dumps({
#   "flattened_sol": flat_sol
# })
# headers = {
#   'Content-Type': 'application/json'
# }

# response = requests.request("POST", missing_checks_endpoint, headers=headers, data=payload, timeout=60*5)
# print(response)
# print(response.text)