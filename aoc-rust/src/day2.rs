use std::collections::HashMap;
use Hand::*;
use RoundResult::*;

lazy_static! {
    static ref BEATS: HashMap<Hand, Hand> =
        HashMap::from([(Rock, Scissors), (Scissors, Paper), (Paper, Rock),]);
}

lazy_static! {
    static ref LOSES: HashMap<Hand, Hand> = HashMap::from_iter(BEATS.iter().map(|(k, v)| (*v, *k)));
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
enum Hand {
    Rock,
    Paper,
    Scissors,
}

impl From<char> for Hand {
    fn from(value: char) -> Self {
        match value {
            'A' => Self::Rock,
            'B' => Self::Paper,
            'C' => Self::Scissors,
            'X' => Self::Rock,
            'Y' => Self::Paper,
            'Z' => Self::Scissors,
            _ => panic!("Bad Hand value"),
        }
    }
}

enum RoundResult {
    Win,
    Loss,
    Draw,
}

impl From<char> for RoundResult {
    fn from(value: char) -> Self {
        match value {
            'X' => Loss,
            'Y' => Draw,
            'Z' => Win,
            _ => panic!("Bad RoundResult value"),
        }
    }
}

struct Round {
    opponent: Hand,
    player: Hand,
}

impl Round {
    fn outcome(&self) -> RoundResult {
        if self.player == self.opponent {
            Draw
        } else if BEATS[&self.player] == self.opponent {
            Win
        } else {
            Loss
        }
    }

    fn score(&self) -> u32 {
        let shape_score = match self.player {
            Rock => 1,
            Paper => 2,
            Scissors => 3,
        };

        let outcome_score = match self.outcome() {
            Loss => 0,
            Draw => 3,
            Win => 6,
        };

        shape_score + outcome_score
    }
}

fn get_incorrect_rounds() -> Vec<Round> {
    let input = include_str!("../puzzle_input/d2").trim();
    input
        .lines()
        .map(|l: &str| Round {
            opponent: l.chars().next().unwrap().into(),
            player: l.chars().nth(2).unwrap().into(),
        })
        .collect()
}

fn get_correct_rounds() -> Vec<Round> {
    let input = include_str!("../puzzle_input/d2").trim();
    input
        .lines()
        .map(|l: &str| {
            let opponent = l.chars().next().unwrap().into();
            let result_needed: RoundResult = l.chars().nth(2).unwrap().into();
            let player_hand = match result_needed {
                Draw => opponent,
                Win => LOSES[&opponent],
                Loss => BEATS[&opponent],
            };

            Round {
                opponent,
                player: player_hand,
            }
        })
        .collect()
}

fn part1() {
    let rounds = get_incorrect_rounds();
    let scores = rounds.into_iter().map(|round| round.score());
    let total_score: u32 = scores.sum();
    println!("{:?}", total_score);
}

fn part2() {
    let rounds = get_correct_rounds();
    let scores = rounds.into_iter().map(|round| round.score());
    let total_score: u32 = scores.sum();
    println!("{:?}", total_score);
}

pub fn run(part: u8) {
    match part {
        1 => part1(),
        2 => part2(),
        _ => println!("Part {} not implemented", part),
    }
}
