use rand::Rng;


/**
    Функция, выполняющая операцию скрещивания двух генотипов.
    Он меняет местами фрагменты генотипов из случайного индекса.
    # Arguments
    * `genotype1` - первый генотип
    * `genotype2` - второй генотип
    # Returns
    Кортеж двух генотипов после операции скрещивания.
 */
pub fn crossover(genotype1: &Vec<[u8; 2]>, genotype2: &Vec<[u8; 2]>) -> (Vec<[u8; 2]>, Vec<[u8; 2]>) {
    let mut rnd = rand::thread_rng();
    let mut result1: Vec<[u8; 2]> = vec![];
    let mut result2: Vec<[u8; 2]> = vec![];
    let random_index = rnd.gen_range(0..genotype1.len());

    for (index, (gen1, gen2)) in genotype1.iter().zip(genotype2.iter()).enumerate(){
        if index >= random_index {
            result1.push(*gen2);
            result2.push(*gen1);
        } else {
            result1.push(*gen1);
            result2.push(*gen2);
        }
    }
    (result1, result2)
}

/**
    Функция, выполняющая операцию мутации генотипа.
    Он меняет случайный бит в случайном гене.
    # Arguments
    * `genotype` - генотип
    # Returns
    Генотип после операции мутации.
 */
pub fn mutation(genotype: &Vec<[u8; 2]>) -> Vec<[u8; 2]> {
    let mut rnd = rand::thread_rng();
    let mut new_genotype: Vec<[u8; 2]> = genotype.clone();
    let random_gen_index = rnd.gen_range(0..new_genotype.len());
    let random_bit = rnd.gen_range(0..7);

    let mut_gen = genotype[random_gen_index];
    let binary_str = format!("{:08b}", mut_gen[1]);
    let mut binary_str = binary_str.chars().collect::<Vec<char>>();
    binary_str[random_bit] = if binary_str[random_bit] == '0' { '1' } else { '0' };
    let new_byte = u8::from_str_radix(&binary_str.iter().collect::<String>(), 2).unwrap();
    new_genotype[random_gen_index][1] = new_byte;

    new_genotype
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_crossover() {
        let genotype1 = vec![[1, 23], [2, 34], [3, 255]];
        let genotype2 = vec![[1, 34], [2, 23], [3, 0]];
        let (result1, result2) = crossover(&genotype1, &genotype2);
        assert_ne!(result1, genotype1);
    }

    #[test]
    fn test_mutation() {
        let genotype = vec![[1, 23], [2, 34], [3, 255]];
        let result = mutation(&genotype);
        assert_ne!(result, genotype);
    }
}