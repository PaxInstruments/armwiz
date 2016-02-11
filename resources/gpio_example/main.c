#include "stm32f10x.h"
#include "stm32f10x_conf.h"

void delay(uint32_t delay_count)
{
	// Delay in miliseconds
	delay_count = delay_count * 6000;
	while (delay_count) {
		delay_count--;
	}
}
void init_led()
{
	GPIO_InitTypeDef GPIO_InitStructure;
	/* GPIOD Periph clock enable */
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOD, ENABLE);

	/* Configure PD2 in output pushpull mode */
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_Init(GPIOD, &GPIO_InitStructure);
}
void gpio_toggle(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
{
	GPIOx->ODR ^= GPIO_Pin;
}
int main(void)
{
	init_led();

	while (1) {
		gpio_toggle(GPIOD, GPIO_Pin_2);
		delay(1000);

	}
}
