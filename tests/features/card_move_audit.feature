Feature: Card move creates audit event
  Scenario: Move card to In Progress
    Given a card exists in Todo
    When I move the card to In Progress
    Then an audit event card_moved is recorded
