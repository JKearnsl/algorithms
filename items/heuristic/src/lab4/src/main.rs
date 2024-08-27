pub mod algorithms;

use std::io;
use std::io::Write;
use rand::Rng;

fn main() {
    let devices = {
        loop {
            print!("Введите количество устройств: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            io::stdin().read_line(&mut input).unwrap();
            match input.trim().parse::<u32>() {
                Ok(n) => break n,
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };
    let tasks = {
        loop {
            print!("Введите количество задач: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            io::stdin().read_line(&mut input).unwrap();
            match input.trim().parse::<u32>() {
                Ok(n) => break n,
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };
    let range: (i32, i32) = {
        loop {
            print!("Введите диапазон значений через запятую: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            match io::stdin().read_line(&mut input) {
                Ok(_) => (),
                Err(_) => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }

            let trimmed_input = input.trim().replace(" ", "");
            let values: Vec<&str> = trimmed_input.split(',').collect();
            if values.len() != 2 {
                println!("Некорректный ввод. Попробуйте еще раз.");
                continue;
            }
            match (values[0].parse::<i32>(), values[1].parse::<i32>()) {
                (Ok(a), Ok(b)) => break (a, b),
                _ => {
                    println!("Некорректный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };

    let matrix = {
        let mut rng = rand::thread_rng();
        let mut temp_matrix = vec![vec![0; devices as usize]; tasks as usize];
        for row in temp_matrix.iter_mut() {
            for cell in row.iter_mut() {
                *cell = rng.gen_range(range.0..range.1);
            }
        }
        temp_matrix
    };

    println!("\nМатрица:");
    for row in matrix.iter() {
        for cell in row.iter() {
            print!("{:4}", cell);
        }
        println!();
    }

    loop {
        println!("\nВыберите тип алгоритма: ");
        println!("\t1. Квадратичный");
        println!("\t2. Кубический");
        println!("\t3. Выход");
        print!("Ваш выбор: ");
        io::stdout().flush().unwrap();
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        match input.trim().parse::<u32>() {
            Ok(n) => {
                match n {
                    1 => {
                        algorithms::quad(&matrix)
                    }
                    2 => {
                        algorithms::cubic(&matrix)
                    }
                    3 => {
                        println!("Выход...");
                        break;
                    }
                    _ => {
                        println!("Некорректный ввод. Попробуйте еще раз.");
                        continue;
                    }
                }
                continue;
            }
            Err(_) => {
                println!("Некорректный ввод. Попробуйте еще раз.");
                continue;
            }
        }
    }
}
