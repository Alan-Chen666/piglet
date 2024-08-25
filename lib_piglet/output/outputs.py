from lib_piglet.output.base_output import base_output
from lib_piglet.output.print_output import print_output
from lib_piglet.output.trace_output import trace_output


outputs = {
    "trace": trace_output,
    "print": print_output,
}
