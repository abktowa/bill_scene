# Project 3: Interactive (Billiard Table) Scene

## Authors
Aban Khan, Shmuel Feld, Matthew Glennon, Jose Salgado, Sai Srujan Vemula, Camryn Keller

## Task assignment
Check out our [group notion page](https://www.notion.so/Project-3-Group-page-1303b34792c48004b53dc1561fd303cf?pvs=4) where we list the project details and assign jobs (Speak to Sam to get access)<br/>

## Consistency guidelines
- **Units**: When drawing our scene, one unit in the coordanite system will correspond to one foot
- **Models**: When creating hierarchical models, objects will be centered along the x and z axes, positioned above the ground level, as if they’re placed on the floor at the y = 0 plane, as shown in the image below.
![demopnstration](https://github.com/user-attachments/assets/562dd0e4-c9a5-4814-aefc-b15df373a29a)
- **Style**: We'll follow standard Python style conventions. Here are some standard Python style guidelines:

    | Element               | Naming Convention | Example                                    |
    |-----------------------|-------------------|--------------------------------------------|
    | **File, Variable, and Function Names** | `snake_case`      | `data_loader.py`, `user_name`, `process_data()` |
    | **Class Names**       | `CamelCase`       | `DataProcessor`, `UserAccount`             |
    | **Constants**         | `ALL_CAPS`        | `MAX_SIZE`, `DEFAULT_TIMEOUT`              |

- **Animation**: We can animate items separately by incrementing separate frame counters for each animated element. When an animation is active, the corresponding frame counter is incremented to create motion over time. Here's an example:

    ```python
    def animation():
        global animate_dice, dice_frame, animate_eight_ball, eight_ball_frame
        if animate_dice:
            dice_frame += 1
        if animate_eight_ball:
            eight_ball_frame += 1
    ```
- **Applying Materials**: Applying materials in the scene is simple. Just use a line like `Materials.set_material(GL_FRONT, Materials.COPPER)` before drawing an object to set its material properties. This material will be applied to all objects drawn afterward until a new material is set. You’ll find plenty of predefined materials in the `Materials` class (like `Materials.SILVER` or `Materials.GOLD`), and you can add your own custom materials there if you want.

- **Switching Between Textures and Materials** *(if you are not texture mapping, no need to worry about this one)*: When using both textures and materials, take care to avoid interference between the two. Use the `Textures` class to apply textures, and be sure to include `glEnable(GL_TEXTURE_2D)` to enable textures and `glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)` to make textures respond to lighting. Additionally, disable materials if they’re not required for the textured object. The `set_material` function in the `Materials` class automatically disables textures, so no further action is needed when switching to a material-only object.

    #### Sample `apply_texture` Method

    ```python
    class Textures:
        @staticmethod
        def apply_texture(texture_id):
            """
            Apply a texture with proper settings for lighting interaction.
            
            Parameters:
            texture_id -- The ID of the texture to bind.
            """
            glEnable(GL_TEXTURE_2D)  # Enable texturing
            glBindTexture(GL_TEXTURE_2D, texture_id)  # Bind the texture
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)  # Allow texture to respond to lighting
            
            # Disable material coloring if not needed for the textured object
            glDisable(GL_COLOR_MATERIAL)
        
        @staticmethod
        def end_texture():
            """Disable texturing after drawing the textured object."""
            glDisable(GL_TEXTURE_2D)
    ```




