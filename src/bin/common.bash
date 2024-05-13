
init() {
    set -euo pipefail
    if is_first_call_to_init ; then return 0 ; fi
    define_PLCC_DIR
    update_PYTHONPATH
    update_CLASSPATH
}

is_first_call_to_init() {
    if [[ -n "${PLCC_FIRST_CALL_TO_INIT:-}" ]] ; then
        return 0
    else
        PLCC_FIRST_CALL_TO_INIT='false'
        export PLCC_FIRST_CALL_TO_INIT
        return 1
    fi
}

define_PLCC_DIR() {
    PLCC_DIR="$( abspath "$( dirname -- "${BASH_SOURCE[0]}" )/../.." )"
    export PLCC_DIR
}

update_PYTHONPATH() {
    PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}${PLCC_DIR}"
    export PYTHONPATH
}

update_CLASSPATH() {
    JACKSON_VERSION="2.15.2"
    JACKSON_ANNOTATIONS="${PLCC_DIR}/plcc/lib/jackson/jackson-annotations-${JACKSON_VERSION}.jar"
    JACKSON_CORE="${PLCC_DIR}/plcc/lib/jackson/jackson-core-${JACKSON_VERSION}.jar"
    JACKSON_DATABIND="${PLCC_DIR}/plcc/lib/jackson/jackson-databind-${JACKSON_VERSION}.jar"
    CP="./Java:${JACKSON_ANNOTATIONS}:${JACKSON_CORE}:${JACKSON_DATABIND}"
    CLASSPATH="${CLASSPATH:+${CLASSPATH}:}${CP}"
    export CLASSPATH
}

abspath() { echo "$( cd -- "${1}" &> /dev/null && pwd )" ; }

assert_file_exists (){
    [ -f "${1}" ] || {
        echo "${1} missing" >&2
        exit 2
    }
}
