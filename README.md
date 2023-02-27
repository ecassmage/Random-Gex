# Random-Gex
Generates random strings based on regex looking syntax


## Supported Syntax

<table>
    <tr>
        <th>[ ]</th>
        <td>
            Acts the same as with regex. All characters contained inside will 
            have an equal chance to be applied to this position.
        </td>
    </tr>
    <tr>
        <th>( )</th>
        <td>Differentiates between layers in the string</td>
    </tr>
    <tr>
        <th>{ }</th>
        <td>Acts as a range between the two integers inputted. ex {1,3} infers that what comes before be repeated 1, 2 or 3 times</td>
    </tr>
    <tr>
        <th>*</th>
        <td>Shorthand for {0,100} (100 is what max_iterations is set to)</td>
    </tr>
    <tr>
        <th>+</th>
        <td>Shorthand for {1,100} (100 is what max_iterations is set to)</td>
    </tr>
</table>

## method Calls
To call the code use
```py
import RSGen


RGex = RSGen.comile('Cat|Dog')
print(RGex.print())  # should print a tree detailing the paths that can be taken by the RSGen
print(RGex.get())  # Should print either Cat or Dog

print(RSGen.get('Cat|Dog'))  # Should print either Cat or Dog
```