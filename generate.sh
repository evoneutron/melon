#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

function usage() {
    echo "Provisions and deploys a project."
    echo "Usage: $0 [--source_dir=SOURCE_DIR]"
    echo "Default: $0 --provision --deploy"
    echo ""
    printf "    %-30s enables checking of the project (default: disabled)\n" "-c, --check"
    printf "    %-30s enables provisioning of the project (default: enabled)\n" "-p, --provision"
    printf "    %-30s enables deployment of the project (default: enabled)\n" "-d, --deploy"
    printf "    %-30s enables verbose logging (-vvv for more, -vvvv to enable connection debugging) (default: disabled)\n" "-v, --verbose"
    printf "    %-30s the environment to deploy (default: \$bamboo_deploy_environment)\n" "--environment"
    printf "    %-30s the playbook to deploy (default: \$bamboo_deploy_project)\n" "--playbook"
    printf "    %-30s the artifact to deploy (default: \$bamboo_deploy_project)\n" "--artifact"
    printf "    %-30s the release to deploy (default: \$bamboo_deploy_release)\n" "--release"
    printf "    %-30s the tarball id used to locate the tarball (default: \$bamboo_deploy_project)\n" "--tarball_id"
    printf "    %-30s the full path to the tarball (default: \$None)\n" "--tarball_path"
    printf "    %-30s the user impersonate (default: ens-deploy)\n" "--user"
    printf "    %-30s the number of hosts to deploy in parallel (default: 1)\n" "--serial"
    printf "    %-30s extra variable to pass to ansible (default: None)\n" "--extra_var"
    printf "    %-30s limit the hosts the playbook is applied to (default: None)\n" "--limit"
    printf "    %-30s lists the hosts that would be deployed, but doesn't deploy (default: None)\n" "--list-hosts"
    printf "    %-30s only run plays and tasks tagged with these values (default: None)\n" "--tags"
    printf "    %-30s display this help message\n" "-h, --help"
}

function run() {

  local temp_var=""

  for var in "$@"; do
    case "$var" in
      -h | --help)
        usage
        exit $E_NOERROR
      ;;

      --source_dir=*)
        source_dir="${var##*=}"
        if [[ "$source_dir" == "" ]]; then
          error "Error: source_dir parameter missing source_dir [$var]"
          echo ""
          usage
          exit $E_WARG
        fi
      ;;

      *)
        warn "Warning: unsupported input parameter [$var]"
      ;;
    esac
  done

  local venv_dir=$ROOT_DIR/venv
  virtualenv -p python3 $venv_dir
  source $venv_dir/bin/activate
  python scripts/imgmelon_generate.py
}

run "$@"