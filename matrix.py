import numpy as np
import plotly.graph_objects as go

#symmetric matrix is matrix A such that A = A^T
def is_symmetric(matrix):
    return np.allclose(matrix, matrix.T)

def apply_transformation(matrix, transformation):
    if transformation == "scale":
        scaling_factor = float(input("Enter the scaling factor: "))
        #multiply the scaling factor by matrix
        return scaling_factor * matrix
    
    elif transformation == "rotate":
        angle = float(input("Enter the rotation angle (in degrees): "))
        theta = np.radians(angle)
        #rotating matrix is given by: [cos(theta), -sin(theta); sin(theta), cos(theta)]
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], 
                                     [np.sin(theta), np.cos(theta)]])
        return rotation_matrix @ matrix @ rotation_matrix.T
    
    elif transformation == "shear":
        shear_factor = float(input("Enter the shear factor: "))
        #shearing matrix is given by: [1, lambda; 0, 1]
        shear_matrix = np.array([[1, shear_factor], [0, 1]])
        return shear_matrix @ matrix @ shear_matrix.T
    else:
        print("Invalid transformation.")
        return matrix

#plots quadratic form of matrix
def plot_quadratic_form(matrix):
    x = np.linspace(-100, 100, 1000)
    y = np.linspace(-100, 100, 1000)

    #N-D coordinate visualization
    X, Y = np.meshgrid(x, y)
    
    #quadratic form of the 2x2 matrix is given by: [x,y]*A*[x;y]
    Z = matrix[0, 0] * X**2 + 2 * matrix[0, 1] * X * Y + matrix[1, 1] * Y**2
    
    #3-D visualization
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
    fig.update_layout(
        title="Quadratic Form Visualization",
        scene=dict(
            xaxis_title="x",
            yaxis_title="y",
            zaxis_title="f(x, y)"
        )
    )

    #writes a separate html page and displays graph
    fig.write_html("matrix.html", auto_open=True)
    #fig.show()


#main 
print("Welcome to the Quadratic Form Visualizer!")
    
#input a 2x2 symmetric matrix
print("Enter a 2x2 symmetric matrix:")
a11 = float(input("Enter a11: "))
a12 = float(input("Enter a12: "))
a21 = float(input("Enter a21: "))
a22 = float(input("Enter a22: "))

#create a new matrix A that has entered elements    
matrix = np.array([[a11, a12], [a21, a22]])
if a12 != a21:
    print("The entered matrix is not symmetric. Exiting.")
    exit()
  
print("Matrix is symmetric. Proceeding...")
print("Select a transformation: scale, rotate, shear")
transformation = input("Enter your choice: ").lower()

#call the function for asing type of transformation
transformed_matrix = apply_transformation(matrix, transformation)
print("Transformed matrix:")
print(transformed_matrix)

#apply transformations to a matrix and plot it
plot_quadratic_form(transformed_matrix)

