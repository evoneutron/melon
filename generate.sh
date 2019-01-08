#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

function usage() {
    echo "Provisions and deploys a project."
    echo "Usage: $0 [--source_dir=SOURCE_DIR]"
    echo "Default: $0 --provision --deploy"
    echo ""
    printf "    %-30s enables checking of the project (default: disabled)\n" "-c, --check"
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