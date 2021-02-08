# Snippet Transformations

## Usage

## Types of Transformations

There are currently two types of transformation supported

- Regular expressions

- Custom function

Please note that both of them operate on the raw snippet text *BEFORE* it is inserted. That means thought it contains things like `$1` and `${2:something}`


### Regular Expressions


### Custom Functions

If you decide to go for a custom function, these function must

- accept a single `str` argument that is going to be the snippet text

- Returns a single string that is going to be the transformed snippet text


For instance, suppose we want 

```python
{
	"raw": R(Key("c-z") + SnippetTransform(lambda s:json.dumps(s).replace("$","\\$"))),
	"almost raw": R(Key("c-z") + SnippetTransform(lambda s:json.dumps(s))),
}
```

### Multiple Successive Transformations Using List


### Picking Up The Transformation From The Extras


```python
mapping = {
	"apply <transformation>":R(Key("c-z") + SnippetTransform("%(transformation)s")),
}

extras = {
	Choice("transformation",{
    		"almost raw": lambda s:json.dumps(s),
    		"raw": lambda s:json.dumps(s).replace("$","\\$"),
    		"alternative raw": [lambda s:json.dumps(s),lambda s:s.replace("$","\\$")], # same effect as above
    		"weird J":(r"\{(\d):i\}",r"\{\1:j\}",),   # regular expression
		}
	)
}
```

Now you may notice that we are using `Key("c-z")` 

Furthermore, you can also write

```python
mapping = {
	"apply <transformation> <transformation2>":R(Key("c-z") + SnippetTransform("%(transformation)s %(transformation2)s")),
}
```

In which case,



## Signature

```python
class SnippetTransform(ActionBase):
	"""Apply a transformation to the previous inserted snippet
	
	Attributes:
	    transformation (
	    		Union[str,Transformation,List[Transformation]] where
	    		Transformation = Union[Tuple,Callable[str,str]]
	    	): 
	    	the transformation to be applied to the last inserted snippet.One of
	    	- callable, that accepts a single parameter the snippet text and 
	    	  returns the final text
	    	- a tuple that describes a regular expression and  contains the arguments
	    	  you would pass to `re.sub` function ( excluding that snippet text of course)

	    	You can also pass at least

	    steps (int): Description
	"""
```



```python
transformations = {
    "almost raw": lambda s:json.dumps(s),
    "raw": lambda s:json.dumps(s).replace("$","\\$"),
    "alternative raw": [lambda s:json.dumps(s),lambda s:s.replace("$","\\$")], # same effect as above
    # simply split into two functions, that will operate one after the other

    "weird J":(r"\{(\d):i\}",r"\{\1:j\}",),   # regular expression
}
```


