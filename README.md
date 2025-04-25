# Python-assessment-ASR-application procedure
Create a command-line interface (CLI) application to track a simple investment portfolio. The 
application should at least allow users to: 
  1. Add assets to the portfolio, specifying the asset ticker (e.g.. AAPL, MSFT), the sector, asset 
     class, quantity, and purchase price. 
  2. Show the current and historical price of each asset ticker and be able to create a graph for 
     each ticker (or a combination of tickers). 
  3. View the current portfolio, displaying each asset's name, sector, asset class, quantity, 
     purchase price,  transaction value and current value. 
  4. See calculations for the total portfolio value and the (relative) weights of each asset including 
     the option to see the same per asset class and sector. 
  5. Be able to perform a simulation over the upcoming fifteen years for the portfolio, 
     demonstrating the impact of risk and uncertainty. Assume 100.000 simulated paths. 
     Use your own creativity to extend the functionality. You are allowed to use a LLM such as ChatGPT to 
     generate ideas.
     
## Technical Requirements 
The following topics are the bare minimum we expect within the assignment, feel free to add 
additional tools to your project. 
  1. Model-View-Controller (MVC) Architecture: 
     The application must adhere to the Model-View-Controller software design pattern: 
       a) Model: stores and manipulates asset information and contains any calculations that 
          are done on this data such as the calculation of weights and other measures. 
       b) View: handles the creation of tables, graphs and optionally the CLI interface itself. 
       c) Controller: manages the flow of data between the Model and View, handling user 
          commands. 
  2. Version Control (Git): The project must be managed using Git, with clear commit messages. 
  3. Dependency Management: The project must have its dependencies specified either through 
     a requirements.txt or through Poetry. 
  4. Programming Language: The preferred programming language is Python but if you are more 
     proficient in a different language such as C++, C# or R this is also a possibility.
     
## Deliverables 
Share with us a public repository on a platform such as GitHub, GitLab or Bitbucket and provide an 
explanation how to use your project. If this is not feasible, a ZIP-file also suffices. It is also important 
that we are able to run the application with your instructions. 
