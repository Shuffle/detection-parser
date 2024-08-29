package main

import (
	"github.com/google/cel-go/common/types/ref"
	"github.com/google/cel-go/common/types"
	"github.com/google/cel-go/common/types/traits"

	"strings"
)

// Custom CEL functions
func icontains(str, substr ref.Val) ref.Val {
    s1, ok1 := str.(types.String)
    s2, ok2 := substr.(types.String)
    if !ok1 || !ok2 {
        return types.Bool(false)
    }
    return types.Bool(strings.Contains(strings.ToLower(string(s1)), strings.ToLower(string(s2))))
}

func any(args ...ref.Val) ref.Val {
    if len(args) != 2 {
        return types.NewErr("any() requires exactly two arguments")
    }

    var iter traits.Iterator
    switch arg0 := args[0].(type) {
    case traits.Iterable:
        iter = arg0.Iterator()
    default:
        // If it's not iterable, treat it as a single-element collection
        // throw an error if it's not a collection
		return types.NewErr("any() requires an iterable as the first argument")
    }

    predicate := args[1]

    for iter.HasNext() == types.True {
        item := iter.Next()
        result := predicate.Equal(item)
        if result == types.True {
            return types.True
        }
    }

    return types.False
}