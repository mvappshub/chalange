Feature: High alert escalation
  Scenario: High alert escalates to incident
    Given a high alert exists
    When I run the watcher once
    Then 1 incident is created
