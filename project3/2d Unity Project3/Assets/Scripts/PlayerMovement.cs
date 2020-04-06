using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public enum StateOfPlayer
{
    walk,
    attack,
    interact

}
public class PlayerMovement : MonoBehaviour
{
    // Varaible for state of player
    public StateOfPlayer playerState;

    // Variable for speed of the player
    public float speed;

    // Variable for rigidbody movement
    private Rigidbody2D rigidBody;

    // Vector for how much players position changes
    private Vector3 changeInPosition;

    // Variable to access the players animations
    private Animator playerAnimations;
    // Start is called before the first frame update
    void Start()
    {
        playerState = StateOfPlayer.walk;
        playerAnimations = GetComponent<Animator>();
        rigidBody = GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    void Update()
    {
        // Every frame resets how much the player has changed
        changeInPosition = Vector3.zero;
        changeInPosition.x = Input.GetAxis("Horizontal");
        changeInPosition.y = Input.GetAxis("Vertical");
        if (Input.GetButtonDown("attack") && playerState != StateOfPlayer.attack) 
        {
            StartCoroutine(AttackCo());
        }
        else if(playerState == StateOfPlayer.walk)
        {
            
            UpdateAnimationAndMovement();
        }
        UpdateAnimationAndMovement();
    }

    private IEnumerator AttackCo()
    {
        playerAnimations.SetBool("attacking", true);
        playerState = StateOfPlayer.attack;
        // Wait for 1 frame
        yield return null;
        // Leave false, otherwise our player goes back into the movement state
        playerAnimations.SetBool("attacking", false);
        yield return new WaitForSeconds(0.3f);
        playerState = StateOfPlayer.walk;
    }
    void UpdateAnimationAndMovement()
    {
        if (changeInPosition != Vector3.zero)
        {
            MoveCharacter();
            playerAnimations.SetFloat("moveX", changeInPosition.x);
            playerAnimations.SetFloat("moveY", changeInPosition.y);
            playerAnimations.SetBool("moving", true);

        }
        else
        {
            playerAnimations.SetBool("moving", false);
        }
    }
    // Function for player movement. Change speed variable in Unity
    void MoveCharacter()
    {
        rigidBody.MovePosition(transform.position + changeInPosition * speed * Time.deltaTime);
    }
}
