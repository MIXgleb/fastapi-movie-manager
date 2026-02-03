#!/bin/bash

set -e

#|-----------------------------------------------------------------------------------------------
#| CONSTANTS
#|-----------------------------------------------------------------------------------------------

readonly COMMAND="${1:-help}"

readonly DOCKER_API_VERSION="v1.42"
readonly DOCKER_SOCKET_PATH="/var/run/docker.sock"
readonly EXCLUDED_AUTO_REMOVAL=("run")

readonly UVICORN_BASE_COMMAND="uvicorn app.main:app"
readonly ALEMBIC_BASE_COMMAND="alembic upgrade head"
readonly SHELL_BASE_COMMAND="python"
readonly PYTEST_BASE_COMMAND="pytest"
readonly HEALTH_BASE_COMMAND="python -m"
readonly HEALTH_ALL_COMMAND="$HEALTH_BASE_COMMAND scripts.health_check.all"
readonly HEALTH_APP_COMMAND="$HEALTH_BASE_COMMAND scripts.health_check.app"
readonly HEALTH_POSTGRES_COMMAND="$HEALTH_BASE_COMMAND scripts.health_check.postgres"
readonly HEALTH_REDIS_COMMAND="$HEALTH_BASE_COMMAND scripts.health_check.redis"

#|-----------------------------------------------------------------------------------------------
#| FUNCTIONS
#|-----------------------------------------------------------------------------------------------

cleanup() {
	is_excluded() {
		local command="$1"
		local excluded
		for excluded in "${EXCLUDED_AUTO_REMOVAL[@]}"; do
			[[ "$command" == "$excluded" ]] && return 0
		done
		return 1
	}

	[ $AUTO_REMOVAL != true ] && return 0
	[ ! -f /.dockerenv ] && return 0
	is_excluded $COMMAND && return 0

	local container_id="$(hostname)"

	echo ""
	echo "🧹 $(colorize "magenta" "Self-destructing container:") $(colorize "yellow" $container_id)"

	if ! curl --unix-socket $DOCKER_SOCKET_PATH -X DELETE \
		"http://localhost/${DOCKER_API_VERSION}/containers/${container_id}?force=true"; then
		echo ""
		echo "┌─────────────────────────────────────────────────────────────"
		echo "│  ⚠️ $(colorize "red" "Could not auto-remove container")"
		echo "│"
		echo "│  💡 $(colorize "yellow" "Possible solutions:")"
		echo "│    1. Check Docker socket: $(colorize "blue" "ls -la $DOCKER_SOCKET_PATH")"
		echo "│    2. Check container: $(colorize "blue" "docker ps -a | grep $container_id")"
		echo "│    3. Manual removal: $(colorize "blue" "docker rm -f $container_id")"
		echo "└─────────────────────────────────────────────────────────────"
	fi
}

colorize() {
	local color="$1"
	local text="${@:2}"

	case "$color" in
	"green") echo -e "\033[1;32m$text\033[0m" ;;
	"yellow") echo -e "\033[1;33m$text\033[0m" ;;
	"blue") echo -e "\033[1;34m$text\033[0m" ;;
	"magenta") echo -e "\033[1;35m$text\033[0m" ;;
	"cyan") echo -e "\033[1;36m$text\033[0m" ;;
	"red") echo -e "\033[1;31m$text\033[0m" ;;
	*) echo "$text" ;;
	esac
}

print_command_with_args() {
	local title="$1"
	shift

	echo "┌─────────────────────────────────────────────────────────────"
	echo "│  🔍 $title"
	echo "│"

	if [ $# -eq 0 ]; then
		echo "│  ⚠️ $(colorize "yellow" "No additional arguments")"
		echo "└─────────────────────────────────────────────────────────────"
		echo ""
		return
	fi

	echo "│  📋 With Arguments:"

	local arg_index=0
	local cur_arg=""
	local arg

	for arg in "$@"; do
		if [[ "$arg" == -* ]]; then
			if [ -n "$cur_arg" ]; then
				arg_index=$((arg_index + 1))
				cur_arg="${cur_arg#' '}"
				echo "│    [$arg_index] $(colorize "green" $cur_arg)"
			fi
			cur_arg="$arg"
		else
			cur_arg="$cur_arg $arg"
		fi
	done

	if [ -n "$cur_arg" ]; then
		arg_index=$((arg_index + 1))
		echo "│    [$arg_index] $(colorize "green" $cur_arg)"
	fi

	echo "└─────────────────────────────────────────────────────────────"
	echo ""
}

#|-----------------------------------------------------------------------------------------------
#| COMMANDS
#|-----------------------------------------------------------------------------------------------

trap cleanup EXIT

EXIT_CODE=0

echo ""
echo "================================"
echo "     🛠️ $(colorize "yellow" "Project Control Hub")"
echo "================================"
echo ""

case "$COMMAND" in
"run")
	echo "🗄️ $(colorize "magenta" "Performing migrations...")"
	echo ""

	$ALEMBIC_BASE_COMMAND

	echo ""
	echo "📦 $(colorize "magenta" "Launching the FastAPI application...")"

	print_command_with_args "Service Launch Command: $(colorize "blue" $UVICORN_BASE_COMMAND)" "${@:2}"
	$UVICORN_BASE_COMMAND "${@:2}"
	;;

"migrate")
	echo "🗄️ $(colorize "magenta" "Performing migrations...")"
	echo ""

	$ALEMBIC_BASE_COMMAND
	;;

"shell" | "python" | "py")
	echo "🐚 $(colorize "magenta" "Launching the Python shell...")"
	echo ""

	$SHELL_BASE_COMMAND
	;;

"test")
	echo "🧪 $(colorize "magenta" "Running the tests...")"

	print_command_with_args "Service Test Command: $(colorize "blue" $PYTEST_BASE_COMMAND)" "${@:2}"
	$PYTEST_BASE_COMMAND "${@:2}"
	;;

"health")
	SERVICE="${2:-all}"

	case "$SERVICE" in
	"all" | ".")
		$HEALTH_ALL_COMMAND
		;;
	"app" | "self" | "fastapi")
		$HEALTH_APP_COMMAND
		;;
	"pg" | "postgres" | "db" | "database")
		$HEALTH_POSTGRES_COMMAND
		;;
	"redis")
		$HEALTH_REDIS_COMMAND
		;;
	*)
		echo "┌─────────────────────────────────────────────────────────────"
		echo "│  🔍 Service Health Check Command: $(colorize "cyan" "health $SERVICE")"
		echo "│"
		echo "│  ❌ Unknown service: $(colorize "red" "$SERVICE")"
		echo "│"
		echo "│  � $(colorize "yellow" "Available services:")"
		echo "│    • $(colorize "cyan" "all|.")                    All services (default)"
		echo "│    • $(colorize "cyan" "app|self|fastapi")         FastAPI application"
		echo "│    • $(colorize "cyan" "pg|postgres|db|database")  PostgreSQL database"
		echo "│    • $(colorize "cyan" "redis")                    Redis cache"
		echo "│"
		echo "│  �� Use $(colorize "cyan" "'help'") to see all available commands"
		echo "└─────────────────────────────────────────────────────────────"

		EXIT_CODE=1
		;;
	esac
	;;

"help" | "-h" | "--help" | "h")
	echo "                         📖 $(colorize "yellow" "AVAILABLE COMMANDS")"
	echo "════════════════════════════════════════════════════════════════════════"
	echo ""
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  $(colorize "cyan" "run [args...]")              $(colorize "magenta" "Launch FastAPI application")"
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  Arguments: OPTIONAL (passed to uvicorn)"
	echo ""
	echo "  $(colorize "yellow" "Default command:")"
	echo "    1. $(colorize "green" $ALEMBIC_BASE_COMMAND)"
	echo "    2. $(colorize "green" "$UVICORN_BASE_COMMAND {args}")"
	echo ""
	echo "  📌 $(colorize "red" "EXAMPLES")"
	echo "    $(colorize "blue" "docker-compose run app run")"
	echo "    $(colorize "blue" "docker-compose run app run --reload")"
	echo "    $(colorize "blue" "docker-compose run app run --host localhost --port 8000")"
	echo ""
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  $(colorize "cyan" "migrate")                    $(colorize "magenta" "Apply database migrations")"
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  $(colorize "yellow" "Runs:")"
	echo "    $(colorize "green" $ALEMBIC_BASE_COMMAND)"
	echo ""
	echo "  📌 $(colorize "red" "EXAMPLES")"
	echo "    $(colorize "blue" "docker-compose run app migrate")"
	echo ""
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  $(colorize "cyan" "shell|python|py")            $(colorize "magenta" "Launch Python interactive shell")"
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  $(colorize "yellow" "Runs:")"
	echo "    $(colorize "green" $SHELL_BASE_COMMAND)"
	echo ""
	echo "  📌 $(colorize "red" "EXAMPLES")"
	echo "    $(colorize "blue" "docker-compose run app py")"
	echo ""
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  $(colorize "cyan" "test [args...]")             $(colorize "magenta" "Run tests")"
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  Arguments: OPTIONAL (passed to pytest)"
	echo ""
	echo "  $(colorize "yellow" "Default command:")"
	echo "    $(colorize "green" "$PYTEST_BASE_COMMAND {args}")"
	echo ""
	echo "  📌 $(colorize "red" "EXAMPLES")"
	echo "    $(colorize "blue" "docker-compose run app test")"
	echo "    $(colorize "blue" "docker-compose run app test tests/test_auth.py -v")"
	echo ""
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  $(colorize "cyan" "health [service]")           $(colorize "magenta" "Health check for services")"
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  Arguments: OPTIONAL (default: 'all')"
	echo ""
	echo "  📝 $(colorize "yellow" "Available services:")"
	echo "    • $(colorize "cyan" "all|.")                    All services (default)"
	echo "    • $(colorize "cyan" "app|self|fastapi")         FastAPI application"
	echo "    • $(colorize "cyan" "pg|postgres|db|database")  PostgreSQL database"
	echo "    • $(colorize "cyan" "redis")                    Redis cache"
	echo ""
	echo "  📌 $(colorize "red" "EXAMPLES")"
	echo "    $(colorize "blue" "docker-compose run app health")"
	echo "    $(colorize "blue" "docker-compose run app health redis")"
	echo "    $(colorize "blue" "docker-compose run app health self")"
	echo ""
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  $(colorize "cyan" "help|-h|--help|h")           $(colorize "magenta" "Show this help (default command)")"
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "  This command is executed by default when no command is provided."
	echo ""
	echo "  📌 $(colorize "red" "EXAMPLES")"
	echo "    $(colorize "blue" "docker-compose run app help")"
	echo ""
	echo "════════════════════════════════════════════════════════════════════════"
	;;

*)
	echo "┌─────────────────────────────────────────────────────────────"
	echo "│  ❌ Unknown command: $(colorize "red" "$COMMAND")"
	echo "│"
	echo "│  💡 Use $(colorize "cyan" "'help'") to see available commands"
	echo "└─────────────────────────────────────────────────────────────"

	EXIT_CODE=1
	;;
esac

exit $EXIT_CODE
