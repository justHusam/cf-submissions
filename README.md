# cf-submissions

Tool to extract set or all public submissions of a [Codeforces](https://codeforces.com) user. Submissions can be filtered based on the programming languages or the verdicts.

## Motivation
I am collecting my Accepted solutions on various online judges to add them to a [GitHub repository](https://github.com/justHusam/Competitive-Programming). I already have a copy of my solutions on online judges that do not save the submissions (e.g. [UVa](https://uva.onlinejudge.org/)), and it is easy to manually collect less than 200 solutions from [SPOJ](https://www.spoj.com/). But collecting more than 1500 solutions from Codeforses manually is not easy at all. So, I have built this tool to extract them.

## Prerequisites

[Python 3.x](https://www.python.org/)


## Installation

1. Download the source code:
```
git clone https://github.com/justHusam/cf-submissions.git
cd cf-submissions
```
2. Install the required modules to run the code:
```
python3 -m pip install -r requirements.txt
```

## Usage

Make sure to navigate to the cf-submissions folder you have downloaded previously.

```
  cf-submissions (-u | --user <user>) [-v | --verdicts <verdict>...] [-l | --languages <language>...]
  cf-submissions -h | --help

options:
  -v, --verdicts <verdict>...   List of submission's verdicts to be extracted   [default=ac]
  -l, --languages <language>... List of submission's languages to be extracted  [default=all]

arguments:
  verdict: 
	all 			- All Verdicts
	ac 			- Ok
	rejected 		- Rejected
	wa 			- Wrong Answer
	rte 			- Runtime Error
	tle 			- Time Limit Exceeded
	mle 			- Memory Limit Exceeded
	ce 			- Compilation Error
	hacked 			- Challenged
	failed 			- Failed
	partial 		- Partial
	pe 			- Presentation Error
	ile 			- Idleness Limit Exceeded
	sv 			- Security Violated
	crashed 		- Crashed
	ipf 			- Input Preparation Failed
	skipped 		- Skipped
	running 		- Running
	pending 		- Submitted
  language:
	all 			- All Languages
	c 			- GNU C
	c11 			- GNU C11
	cpp.clang++-diagnose 	- Clang++17 Diagnostics
	cpp 			- GNU C++
	c++0x 			- GNU C++0x
	cpp11 			- GNU C++11
	cpp14 			- GNU C++14
	cpp17 			- GNU C++17
	cpp.g++17-drmemory 	- GNU C++17 Diagnostics
	cpp.ms 			- MS C++
	csharp.mono 		- Mono C#
	csharp.ms 		- MS C#
	d 			- D
	go 			- Go
	haskell 		- Haskell
	java6 			- Java6
	java7 			- Java7
	java8 			- Java8
	kotlin 			- Kotlin
	ocaml 			- Ocaml
	pas.dpr 		- Delphi
	pas.fpc 		- FPC
	pas.pascalabc 		- PascalABC.NET
	perl 			- Perl
	php 			- PHP
	py2 			- Python 2
	py3 			- Python 3
	pypy2 			- PyPy 2
	pypy3 			- PyPy 3
	ruby 			- Ruby
	rust 			- Rust
	scala 			- Scala
	js 			- JavaScript
	nodejs 			- Node.js
	cobol 			- Cobol
	mysterious 		- Mysterious Language
	secret171 		- secret_171
	ada 			- Ada
	qsharp 			- Q#
	tcl 			- Tcl
	false 			- False
	io 			- Io
	pike 			- Pike
```

## Examples

Make sure to navigate to the cf-submissions folder you have downloaded previously.

1. Extract all Accepted solutions of the user [justHusam](https://codeforces.com/profile/justHusam):
```
python3 cf-submissions.py -u justHusam
```

2. Extract all GNU C++11 Accepted submissions of the user [justHusam](https://codeforces.com/profile/justHusam):
```
python3 cf-submissions.py -u justHusam -l cpp11
```

3. Extract all GNU C++11 and Java 8 Accepted submissions of the user [justHusam](https://codeforces.com/profile/justHusam):
```
python3 cf-submissions.py -u justHusam -l cpp11 java8
```

4. Extract all Wrong Answer solutions of the user [justHusam](https://codeforces.com/profile/justHusam):
```
python3 cf-submissions.py -u justHusam -v wa
```

5. Extract all Accepted and Wrong Answer solutions of the user [justHusam](https://codeforces.com/profile/justHusam):
```
python3 cf-submissions.py -u justHusam -v ac wa
```

6. Extract all GNU C++11 and Java 8 Accepted and Wrong Answer submissions of the user [justHusam](https://codeforces.com/profile/justHusam):
```
python3 cf-submissions.py -u justHusam -l cpp11 java8 -v ac wa
```

7. Print help message:
```
python3 cf-submissions.py -h
```
## License

This project is licensed under the MIT License.
