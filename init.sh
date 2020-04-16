SCRIPT_PATH=$(pwd)
${SCRIPT_PATH}/init_submodule.sh dns_resolver git@github.com:ChenZaichuang/DNS-Resolver.git
pip install -r ${SCRIPT_PATH}/requirements.txt