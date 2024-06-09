import getopt
import shlex

import regex

"""
Investigating methods to tokenize command line input for search and 
classification.

Not really a usable file, just collecting my notes/methods for an 
implementation to follow.
"""

# For example:
t = 'ls -la ~; echo "Hello World"'
s = shlex.shlex(t, posix=True, punctuation_chars=True)
s.whitespace_split = True
print(list(s))

def simple_lex(string):
  result = shlex.shlex(string, posix=True, punctuation_chars=True)
  result.whitespace_split = True
  return list(result)

def group_commands(token_list):
  command_delimiters = ';|&' # What else belongs here?
  group = []
  for token in token_list:
    group.append(token)
    if token in command_delimiters:
      yield group
      group = []
    """
    Could identify redirections here. '>' and '>>' - what else? When a 
    redirect operator is found, can we assume it will be followed by 
    the above characters in command_delimiters (or the end of string)? 
    Or do we need a contextual syntax to consume tokens following a 
    redirect operator? Might it be clearer to break apart redirection 
    constructs in a separate utility function?
    """
  yield group
  
def split_terminator(token_list):
  """
  Separate a token list into a shell command and any optional redirect 
  statements or assignment words that may follow (or precede!?) it.
  
  The trick here is that redirect operators can sometimes be prefixed 
  by a file descriptor number, but whitespace is not guaranteed, and 
  if the number is escaped it should not be captured by the redirect 
  statement and instead be interpreted as part of the command.
  
  Also note that assignment words may prefix a command in addition to 
  redirect statements. Assignment words are of the form '\w+=\w+' and 
  represent a temporary assignment to the shell environment where the 
  following command will be executed.
  """
  command_terminators = ';<>|&'

def is_assignment(token):
  """
  Predicate to identify tokens as assignment words, which are of the 
  form '\w+=\w+'.
  """
  return regex.match(r'\w+=\w+', token) != None

"""
How to do the same for redirect statements? It may be necessary to 
search for redirections before splitting tokens, because white space 
can't be reconstructed. Or would it be better to split without looking 
for special punctuation first, then search and modify the resulting 
tokens? This seems susceptible to complications from quote/escape 
expansion, so perhaps modifying the text before tokenization is the 
better option to start.
"""

"""
Specifications:
  - Considering the case of a single (not composed) command, the token 
    in the [0] position is the executable path. The remainder [1:] is 
    the argument list, to be handled by getopt.
  - Arguments are options when preceded by a hyphen '-'. Multiple 
    options may follow a hyphen within a single token if the options do 
    not take arguments.
    - Option names must be a single alphanumeric character. 
    - getopt captures options and separates them into individual 
      containers whether they are specified individually or together in 
      a single token.
  - Options specified individually may be followed by arguments, either 
    as the remainder of the option token (catenated) or in the 
    following token (ie with white space after the option token). 
    - getopt cannot automatically recognize the equivalency without 
      being instructed, and because we do not know the syntax of the 
      commands to be parsed in advance, we will have to devise a 
      separate strategy for splitting arguments from option tokens when 
      presented as a single string.
  - A double hyphen ('--') token indicates the end of the options list; 
    any further tokens are treated as non-option arguments, even if 
    they begin with a hyphen and would otherwise be matched as an 
    option. getopt handles this behavior automatically.
  - A token containing only a single hyphen is treated as a literal 
    argument. getopt handles this behavior automatically.
    - Convention is to use a hyphen to represent a default stream 
      (stdin or stdout) for parameters that take path-like parameters 
      but can also interact directly with standard IO. It has no fixed 
      meaning, however.
  - Options can appear multiple times, in arbitrary order. getopt 
    handles this behavior automatically.
  - GNU conventions also allow long options, specified by a name 
    prefixed with a double hyphen. 
    - Unlike "short" options, long options must be specified 
      individually. Long options arguments are to be specified by using 
      an equals sign as a delimiter ('--opt=arg') but it's not clear 
      whether or not some commands may allow arguments in a separate 
      token after the long option ('--opt arg') in the fashion of short 
      options.
    - Long options may be abbreviated. It's unclear whether or not this 
      specification is followed in practice. getopt does support this 
      behavior, but it is not automatic. We will need a means for 
      milestone authors to provide some configuration hints about the 
      long options we're searching for, because getopt needs a list of 
      long option names to check against in order to identify 
      abbreviations.
    - Authors will need to research commands and include not only the 
      target long option identifiers, but also any other long options 
      whose names might overlap the target in a partial match. We 
      should investigate the priority given to ambiguous partial 
      matches if we can find some practical examples, and consider ways 
      to patch this behavior in the future as specific requirements are 
      discovered.
  - The POSIX and GNU specifications on syntax are really just 
    guidelines/conventions. We should keep in mind while designing that 
    some commands, especially older ones predating these conventions, 
    might have idiosyncrasies that are inescapable for our scenario 
    designers. 
    - If at all possible, we should choose an approach that allows 
      future authors to inject helper methods to do special preparation 
      and/or cleanup on commands with weird calling conventions. 
    - This might be accomplished by a callback registry, an optional 
      lexing table, or by subclassing the lexer and providing a custom 
      lexer instance when the scenario sets up the milestone 
      interpreter.
    - Whatever the structure, I think we should leverage Python's 
      first-class functions and base the strategy on injecting custom 
      methods into the existing lexer behavior, as opposed to 
      data-driven representation. A data-driven approach would require 
      us to anticipate what potential problems might look like, and I 
      don't think it'd be a good use of time unless we could turn up 
      some examples of problems to be fixed. It's more conservative to 
      just reserve flexible entry points in places where it's 
      convenient to the existing design rather than throwing up data 
      type scaffolding in hopes we'll use it later on.
    - We don't need to support all syntax for all commands - just the 
      syntax of the commands our authors want to search for. It's the 
      future wants we need to be wary of.
References:
  - https://www.gnu.org/software/libc/manual/html_node/
    Argument-Syntax.html
  - https://www.gnu.org/software/libc/manual/html_node/Getopt.html
  - https://www.gnu.org/prep/standards/standards.html
    #Command_002dLine-Interfaces
  - https://pubs.opengroup.org/onlinepubs/9699919799/utilities/
    V3_chap02.html
    - Part 2.10 explains shell grammar in detail.
  - https://docs.python.org/3/library/getopt.html
  - https://docs.python.org/3/library/shlex.html
Notes:
  - Helpful semantics from Open Group's shell command language 
    specification document:
    - Pipes and and-or clauses belong to the pipeline grammar.
    - Compound commands encompass brace-groups, subshells, and for, 
      case, if, while and until clauses.
    - 
  - POSIX and/or GNU do not seem to specify any requirements on the 
    interpretation of order of arguments - meaning that our prior 
    assumption that we can alphabetize options is not guaranteed to 
    hold for all commands. An alternative solution would be to provide 
    a search method that preserves argument order for sensitive cases, 
    and for more general use implement an order-free search based on 
    set membership. To support commands that distinguish repetition of 
    short options ('-fff' or '-vvv') we can use multisets.
    - Many commands do allow some reordering of options and other 
      arguments, but this is generally due to the behavior of libraries 
      in specific C flavors, such as GNU C. It is not specified in any 
      particular requirements and its implementation may conceivably 
      vary with the library and execution environment.
  - On recognizing redirection operations:
    - Constructs to look for: '<', '<&', '<<', '<<<', '<<-', '<>', '>', 
      '>|', '>&', '>>', '|', '||', '&&'. What about alternatives 
      specific to particular shells, such as '>!' as an alternative of 
      '>|', or '|&' being equivalent to '2>&1 |'?
    - Quoted elements of a redirection statement should be excluded and 
      considered part of the preceding command (eg 'echo \2>a' is  
      tokenized as ['echo', '\2'], ['>a']).
  - Given the fragility and ambiguity of some of the issues discussed 
    here, I think we should consider the idea of conventions for 
    student users, and not just developers and/or instructors/
    customers.
    - This would be in the form of some guidelines on how we would 
      prefer and expect students to interact with the scenarios. For 
      instance, an informal guideline we already use is that edurange 
      is a training delivery system, not a CTF - we ask that students 
      not attack the infrastructure, and trust that everyone complies 
      for the sake of our shared productivity.
    - Similarly, we are on the cusp of making some asks about students 
      using the chat and online help systems.
    - We could document these asks as a preamble that's presented 
      whenever students join an instance or scenario, and/or put a 
      prominent link the scenario UI where student users can review it 
      at their leisure.
    - An example ask relevant to log analysis might include policies on 
      when and where to use composed commands (if they prove to be 
      difficult to support with regard to milestone analysis). 
    - Another application might be giving a brief overview of how the 
      milestones, online help and scenario question systems are related 
      and how we use that information to understand what students are 
      doing. If students have some context for how their attempts 
      contribute to our data, they might be more motivated to cooperate 
      with our instructions.
Proposals:
  - Shells allow comments. I knew this from shell script, but don't 
    typically think about it in daily CLI use. Who would read a comment 
    on the command line, after all? But what if we allowed comments as 
    a way for users to flag commands for help, or even to automatically 
    create a chat message referring instructors (or the ML help system) 
    to that log line? shlex automatically separates comments, so 
    providing an entry point for this behavior would be trivial.
  - Would it be possible to reverse engineer our tokenization process 
    so that it could be performed automatically (naïvely) with just a 
    sample string as input?
    - For instance, when a command includes no options, the arguments 
      then all lack labels, and thus can be treated unambiguously as 
      positional and identified by their order. 'man chmod', for 
      instance, can easily be handled automatically.
    - It seems plausible that short options, and non-overlapping long 
      options, could be inferred in similar ways, argument ambiguities 
      notwithstanding.
    - It would be up to the author to know where this representation 
      falls short. For instance, an automatic search for 'ls' might 
      also permit options ('ls -la') or parameters ('ls path') that 
      change behavior in ways the milestone author did not intend.
Questions:
  - shlex makes it simple to break strings on characters that would 
    indicate separate shell commands, such as ';' and '>', but making 
    use of that distinction begs questions of how we would treat such a 
    composed set of commands in log output.
    - Would each command in the composition be logged separately? How 
      would they then be indexed? Presumably the goal of splitting the 
      input would be to evaluate each command against milestones 
      separately. And would this preclude designing milestones that 
      explicitly require composed commands?
  - How flexible do we want to be about how an executable is called - 
    ie if a user writes '/bin/cat' instead of 'cat', do we want to try 
    to allow that automatically, or is it OK that the milestone 
    interpreter will reject a working variation of a command?
    - If we were to implement a solution to the above, how would we 
      treat situations like the 'Trojan cat' in the strace scenario, 
      where the PATH setup makes the two permutations non-equivalent 
      (eg they actually point to different commands despite 
      appearances)?
  - There seems to be a deep ambiguity inherent in the ability for 
    options to consume arguments. 
    - This is compounded by the convention of options generally being 
      specified before positional arguments. 
    - It seems likely that we will not be able to find a general-
      purpose way to distinguish the user's intent/the command's 
      syntax. Can we provide a way for the milestone author to provide 
      hints to getopt? 
    - getopt does have some facility to specify that an option requires 
      an argument. What is a good way to expose this parameter to the 
      milestone author? How much coverage does it provide for the problem 
      at hand?
    - Are there also cases where an option can take an argument 
      optionally? If so, how can we handle such cases?
  - How do redirection constructs affect our search needs for milestone 
    development?
    - Do we anticipate a need for identifying what is redirected, and 
      not merely how it is redirected?
    - Is it sufficient to make the redirect statement available to the 
      milestone author?
    - The lexer should probably distinguish the command from whatever 
      terminates it, either ';' or a redirect statement, but make those 
      terminating tokens are available for analysis.
  - How should grouping lists (commands enclosed in parentheses or 
    curly braces) be handled? Like other sequences of commands? What 
    about control flow constructs based on these groups?
  - In the Open Group shell specification grammar, there is the 
    substitution 'cmd_suffix -> WORD'. What is the meaning of a lone 
    word after a command clause?
    - Is this how the shell grammar represents argument input to the 
      command to be called? Does that imply that command arguments and 
      redirection statements can be intermixed?
To Do:
  - Check that '\w+=\w+' properly captures only the allowed characters 
    for assignment words per the Open Group specification.
"""