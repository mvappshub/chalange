Feature: High alerts get escalated
  Scenario: Create high alert then escalate via watcher logic (service)
    Given I create a high alert
    Then the alert is stored
