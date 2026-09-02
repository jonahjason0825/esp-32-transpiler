#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"


void app_main(void)
{
    gpio_reset_pin(12); gpio_set_direction(12, GPIO_MODE_OUTPUT); gpio_set_level(12, 1);
    vTaskDelay(pdMS_TO_TICKS(100));
    gpio_reset_pin(12); gpio_set_direction(12, GPIO_MODE_OUTPUT); gpio_set_level(12, 0);
    vTaskDelay(pdMS_TO_TICKS(100));
    printf("Current time: %ld\n", esp_timer_get_time());
    gpio_reset_pin(12);gpio_set_direction(12, GPIO_MODE_OUTPUT);gpio_set_level(12, 1);
    printf("Available DRAM: %d bytes\n", esp_get_free_heap_size());

    while (1){
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
