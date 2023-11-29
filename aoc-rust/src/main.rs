mod day1;

use clap::Parser;

#[derive(Parser)]
#[command(author, version, about)]
struct Cli {
    #[arg(short, long, value_name = "DAY")]
    day: u8,

    #[arg(short, long, value_name = "PART")]
    part: u8,
}

fn main() {
    let cli = Cli::parse();

    match cli.day {
        1 => day1::run(cli.part),
        _ => println!("Day {} not implemented", cli.day),
    }
}
