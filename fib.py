import argparse

def fib(n):
	a, b = 0,1
	for i in range(n):
		a,b = b, a+b
	return a

def main():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-v','--verbose',action='store_true')
	group.add_argument('-q','--quiet',action='store_true')
