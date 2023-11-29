pub fn run(part: u8) {
    match part {
        1 => part1(),
        // 2 => part2(),
        _ => println!("Part {} not implemented", part),
    }
}

fn part1() {
    let input = include_str!("../puzzle_input/d1");
    println!("{}", input);
}
