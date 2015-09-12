# Sol

Sol is a prototype language based on [Io Language](http://iolanguage.org/).

The codebase is pre-alpha. Everything's in flux and the code is pretty ugly. Use at your own risk.

## Install & run

    $ git clone https://github.com/ianpreston/sol
    $ cd sol && virtualenv venv && source venv/bin/activate
    $ py.test sol/
    $ python main.py


## Hello world

    >>> x := "Hello, world!"
    >>> x.println
    Hello, world!


## License

Available under the [MIT License](http://opensource.org/licenses/MIT).
