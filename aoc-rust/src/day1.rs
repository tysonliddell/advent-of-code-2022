pub fn run(part: u8) {
    match part {
        1 => part1(),
        2 => part2(),
        _ => println!("Part {} not implemented", part),
    }
}

struct Elf {
    item_calories: Vec<u32>,
}

impl Elf {
    fn total_calories(&self) -> u32 {
        self.item_calories.iter().sum()
    }
}

fn get_elves() -> Vec<Elf> {
    let input = include_str!("../puzzle_input/d1").trim();
    input
        .split("\n\n")
        .map(|s: &str| {
            let items: Vec<u32> = s
                .split('\n')
                .map(|num| num.parse::<u32>().expect("Numbers should parse!"))
                .collect();
            Elf {
                item_calories: items,
            }
        })
        .collect()
}

fn part1() {
    let most_calories = get_elves()
        .into_iter()
        .map(|e| e.total_calories())
        .max()
        .expect("There should be a max calories elf!");
    println!("{}", most_calories);
}

fn part2() {
    let mut calories_list: Vec<u32> = get_elves()
        .into_iter()
        .map(|e| e.total_calories())
        .collect();
    calories_list.sort();
    let top_3_sum: u32 = calories_list.into_iter().rev().take(3).sum();
    println!("{}", top_3_sum);
}
