Feature: Moving a card writes audit log
  Scenario: Move card from Backlog to In Progress
    Given I have the default board
    And I create a card in list "Backlog"
    When I move the card to list "In Progress"
    Then audit contains action "card_moved"
