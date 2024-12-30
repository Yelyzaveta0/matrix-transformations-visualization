import numpy as np
import plotly.graph_objects as go

#symmetric matrix is matrix A such that A = A^T
def is_symmetric(matrix):
    return np.allclose(matrix, matrix.T)

def is_conistic(matrix):
    determinant = np.linalg.det(matrix)
    eigenvalues = np.linalg.eigvals(matrix)

    if determinant > 0 and np.all(eigenvalues > 0):
        return "Ellipse"
    elif determinant > 0 and np.all(eigenvalues < 0):
        return "Ellipse (indefinite)"
    if determinant < 0:
        return "Hyperbola"
    if determinant == 0:
        return "Parabola"

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
def plot_quadratic_form(matrix, shape):
    if shape == "Ellipse":
        x = np.linspace(-10, 10, 200)
        y = np.linspace(-10, 10, 200)
    elif shape == "Hyperbola":
        x = np.linspace(-50, 50, 400)
        y = np.linspace(-50, 50, 400)
    elif shape == "Parabola":
        x = np.linspace(-20, 20, 400)
        y = np.linspace(-10, 10, 400)
    else:
        x = np.linspace(-10, 10, 200)
        y = np.linspace(-10, 10, 200)
    #N-D coordinate visualization
    X, Y = np.meshgrid(x, y)
    Z = matrix[0, 0] * X**2 + 2 * matrix[0, 1] * X * Y + matrix[1, 1] * Y**2
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="YlGnBu")])

    #set initial axis ranges
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-10, 10]),
            yaxis=dict(range=[-10, 10]),
            zaxis=dict(range=[-100, 100]),
        )
    )

    #add dropdown menu for preset ranges
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Default Range",
                        method="relayout",
                        args=[
                            {
                                "scene.xaxis.range": [-10, 10],
                                "scene.yaxis.range": [-10, 10],
                                "scene.zaxis.range": [-100, 100],
                            }
                        ],
                    ),
                    dict(
                        label="Wide Range",
                        method="relayout",
                        args=[
                            {
                                "scene.xaxis.range": [-50, 50],
                                "scene.yaxis.range": [-50, 50],
                                "scene.zaxis.range": [-500, 500],
                            }
                        ],
                    ),
                    dict(
                        label="Close Range",
                        method="relayout",
                        args=[
                            {
                                "scene.xaxis.range": [-5, 5],
                                "scene.yaxis.range": [-5, 5],
                                "scene.zaxis.range": [-50, 50],
                            }
                        ],
                    ),
                ],
                direction="down",
                showactive=True,
            )
        ]
    )

    #sliders for axis ranges
    sliders = [
        dict(
            active=2,
            currentvalue={"prefix": "X Range: "},
            steps=[
                dict(
                    label=f"[{start}, {start + 20}]",
                    method="relayout",
                    args=[
                        {
                            "scene.xaxis.range": [start, start + 20],
                        }
                    ],
                )
                for start in range(-50, 51, 10)
            ],
        ),
        dict(
            active=2,
            currentvalue={"prefix": "Y Range: "},
            steps=[
                dict(
                    label=f"[{start}, {start + 20}]",
                    method="relayout",
                    args=[
                        {
                            "scene.yaxis.range": [start, start + 20],
                        }
                    ],
                )
                for start in range(-50, 51, 10)
            ],
        ),
    ]

    fig.update_layout(sliders=sliders)
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
shape = is_conistic(transformed_matrix)
print(f"The shape is: {shape}")

#apply transformations to a matrix and plot it
plot_quadratic_form(transformed_matrix, shape)