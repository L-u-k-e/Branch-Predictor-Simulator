# Branch-Predictor-Simulator
Simulates 3 different types of branch prediction given a set of results to test their accuracy


Simulates 3 different types of branch prediction, given an input file of actual branching results.

 - Fixed   (always picks true)
 - Static  (first taken)
 - dynamic (two layer adaptive learner)
 

Input file needs to be formatted like

    branch address\t[@.]]\ttarget address

Where `@` means the branch was taken and `.` means it wasnt. So for example:

    0x7fa5af528cd3	@	0x7fa5af52cc30
    0x7fa5af52cc7f	.	0x7fa5af52cc85
    0x7fa5af52ccc1	@	0x7fa5af52ccdf
    0x7fa5af52cce3	@	0x7fa5af52ccc8
    0x7fa5af52ccdd	.	0x7fa5af52ccdf
    
Run like:
  
   python3 input.trace
