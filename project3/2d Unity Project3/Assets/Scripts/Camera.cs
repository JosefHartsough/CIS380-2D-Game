using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Camera : MonoBehaviour
{

    public Transform cameraPos;

    // Variable for speed of the camera movement
    public float speedOfCameraMovement;

    // Variables for the max position for camera, and min position
    public Vector2 maxPosition;
    public Vector2 minPosition;
    // Start 
    void Start()
    {
        
    }

    // LateUpdate is being used because we want our player to move in update first before the camera
    // Lerp is used to move towards position. Find distance between itself and target position and moves
    void LateUpdate()
    {
        if(transform.position != cameraPos.position)
        {
            Vector3 cameraPosition = new Vector3(cameraPos.position.x, cameraPos.position.y, transform.position.z);  

            // 3 Arguemnets 1:position we are at currently, 2:position we want to move to, 3:amount we want to cover 
            transform.position = Vector3.Lerp(transform.position, cameraPosition, speedOfCameraMovement);
        }
    }
}
