#
#	rhsmcertd bash completion script
#	  based on rhn-migrate-classic-to-rhsm bash completion script
#

# main completion function
_rhsmcertd()
{
	local first cur prev opts base
	COMPREPLY=()
	first="${COMP_WORDS[1]}"
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"
	opts="-h --help -c --cert-check-interval -d --debug -n --now -s --no-splay -a --auto-registration -r --auto-registration-interval"

	case "${cur}" in
		-*)
			COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
			return 0
			;;
	esac

	COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
	return 0
}

complete -F _rhsmcertd rhsmcertd
