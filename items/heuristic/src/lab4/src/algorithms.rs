use std::io;
use std::io::Write;

use rand::seq::SliceRandom;

fn column_els(matrix: &Vec<Vec<i32>>, column: usize) -> Vec<i32> {
    matrix.iter().map(|row| row[column]).collect()
}

fn pow_unicode(pow: u32) -> &'static str {
    match pow {
        2 => "²",
        3 => "³",
        _ => "ⁿ",
    }
}

fn logic(matrix: &Vec<Vec<i32>>, pow: u32) {
    let mut buffer_matrix = vec![vec![0; matrix[0].len()]; matrix.len()];
    let mut buffer_device_tasks = vec![vec![0; matrix[0].len()]; matrix[0].len()];
    let unicode_pow: &str = pow_unicode(pow);
    for (i, row) in matrix.iter().enumerate() {
        println!("\nШаг {}\n", i + 1);
        for (ri, device) in buffer_device_tasks.iter_mut().enumerate() {
            print!("[У №{}] ", ri + 1);

            device[ri] = row[ri];
            for (ci, task) in device.iter_mut().enumerate() {
                let sum_col = column_els(&buffer_matrix, ci).iter().sum::<i32>();
                if sum_col != 0 {
                    print!("({}+{}){:3} ", sum_col, task, unicode_pow);
                }else {
                    print!("{}{:3}", task, unicode_pow);
                }
                *task = (sum_col + *task).pow(pow);
            }
            print!("| Сумма: {}", device.iter().sum::<i32>());
            println!();
        }
        let min_task_index = buffer_device_tasks.iter().enumerate().min_by_key(
            |(_, row)| row.iter().sum::<i32>()
        ).unwrap().0;
        buffer_matrix[i][min_task_index] = matrix[i][min_task_index];
        println!("Мин №{}", min_task_index + 1);
        println!();
        buffer_device_tasks = vec![vec![0; matrix[0].len()]; matrix[0].len()];
        for r in buffer_matrix.as_slice()[0..i+1].iter() {
            for c in r.iter() {
                print!("{:4} ", c);
            }
            println!();
        }
        println!();
    }

    println!("Результат:");
    let mut results = vec![0; matrix[0].len()];
    for i in 0..matrix[0].len() {
        results[i] = column_els(&buffer_matrix, i).iter().sum::<i32>();
        print!("{} ", results[i]);
    }
    print!("Max: {}", results.iter().max().unwrap());
    println!();
}

pub fn quad(input_matrix: &Vec<Vec<i32>>) {
    let matrix = {
        let mut temp_matrix = input_matrix.clone();
        loop {
            println!("\nКак отсортировать матрицу?");
            println!("\t1. В случайном порядке");
            println!("\t2. По возрастанию");
            println!("\t3. По убыванию");
            print!("Ваш выбор: ");
            io::stdout().flush().unwrap();
            let mut choice = String::new();
            io::stdin().read_line(&mut choice).unwrap();
            let choice: u32 = match choice.trim().parse() {
                Ok(num) => num,
                Err(_) => {
                    println!("Неверный ввод. Попробуйте еще раз.");
                    continue;
                }
            };
            match choice {
                1 => {
                    let mut rng = rand::thread_rng();
                    temp_matrix.shuffle(&mut rng);
                    break temp_matrix;
                },
                2 => {
                    temp_matrix.sort_by_key(|row| row.iter().sum::<i32>());
                    break temp_matrix;
                },
                3 => {
                    temp_matrix.sort_by_key(|row| -row.iter().sum::<i32>());
                    break temp_matrix;
                },
                _ => {
                    println!("Неверный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };

    println!("\nОтсортированная матрица:");
    for row in matrix.iter() {
        for cell in row.iter() {
            print!("{:4} ", cell);
        }
        print!("\t| Сумма: {}", row.iter().sum::<i32>());
        println!();
    }

    logic(&matrix, 2);
}

pub fn cubic(input_matrix: &Vec<Vec<i32>>) {
    let matrix = {
        let mut matrix = input_matrix.clone();
        loop {
            println!("\nКак отсортировать матрицу?");
            println!("\t1. По убыванию");
            print!("Ваш выбор: ");
            io::stdout().flush().unwrap();
            let mut choice = String::new();
            std::io::stdin().read_line(&mut choice).unwrap();
            let choice: u32 = match choice.trim().parse() {
                Ok(num) => num,
                Err(_) => {
                    println!("Неверный ввод. Попробуйте еще раз.");
                    continue;
                }
            };
            match choice {
                1 => {
                    matrix.sort_by(|a, b| b.cmp(a));
                    break matrix;
                }
                _ => {
                    println!("Неверный ввод. Попробуйте еще раз.");
                    continue;
                }
            }
        }
    };

    println!("\nОтсортированная матрица:");
    for row in matrix.iter() {
        for cell in row.iter() {
            print!("{} ", cell);
        }
        println!();
    }

    logic(&matrix, 3);
}