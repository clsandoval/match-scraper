STRATZ_GRAPHQL_URL="https://api.stratz.com/graphql"
OPENDOTA_URL = "https://api.opendota.com/api/"

QUERY_HEADER={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

new_end_graphql_query = """]) {
    id
    startDateTime
    players{
      heroId
      leaverStatus
    	stats{
        assistEvents{
          time
        }
        deathEvents{
          time
        }
        killEvents{
          time
        }
      	lastHitsPerMinute
        networthPerMinute
        experiencePerMinute
        deniesPerMinute
        heroDamagePerMinute
        actionsPerMinute
        heroDamageReceivedPerMinute
      }
    }
  }
}
    """


start_graphql_query = """{
  matches(ids: [
    """
end_graphql_query ="""]) {
        id
        startDateTime
        lobbyType
        gameMode
        actualRank
        analysisOutcome
        durationSeconds
    		towerStatusDire
    		towerStatusRadiant
    		barracksStatusDire
    		barracksStatusRadiant
        firstBloodTime
        players{
        steamAccount{
          isAnonymous
        }
        steamAccountId
        partyId
        item0Id
        item1Id
        item2Id
        item3Id
        item4Id
        item5Id
        dotaPlus{
          level
        }
      	hero{
          name
        }
        leaverStatus
      	stats{
          tripsFountainPerMinute
          deathEvents{
            timeDead
          }
          healCount
          wardDestruction{
            time
          }
          deathCount
          killCount
          heroDamageReport{
            dealtTotal{
              physicalDamage
              magicalDamage
              disableDuration
            }
            receivedTotal{
              physicalDamage
              magicalDamage
              disableDuration
            }
          }
          towerDamageReport{
            damage
          }
          courierKills{
            time
          }
        	}
        }
      }
    }"""


player_specific_graphql_query="""{
  players(steamAccountIds:["""

player_specific_graphql_query_end = """]) {
    steamAccountId
		winCount
    matchCount
    behaviorScore
    heroesPerformance(take: 130){
      hero {
        name
        id
      }
      winCount
      matchCount
      kDA
      duration
    }
    heroStreaks{
      heroId
      longestStreak
      currentStreak
    }
  } 
}"""