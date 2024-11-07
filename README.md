# Project 3: Interactive (Billiard Table) Scene

## Authors
Aban Khan, Shmuel Feld, Matthew Glennon, Jose Salgado, Sai Srujan Vemula, Camryn Keller

## Task assignment
Check out our [group notion page](https://www.notion.so/Project-3-Group-page-1303b34792c48004b53dc1561fd303cf?pvs=4) where we list the project details and assign jobs (Speak to Sam to get access)<br/>

## Consistency guidelines
- When drawing our scene, one unit in the coordanite system will correspond to one foot
- When creating hierarchical models, objects will be centered along the x and z axes, positioned above the ground level, as if they’re placed on the floor at the y = 0 plane, as shown in the image below.
![demopnstration](https://github.com/user-attachments/assets/562dd0e4-c9a5-4814-aefc-b15df373a29a)
- We'll follow standard Python style conventions. Here are some standard Python style guidelines:

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





