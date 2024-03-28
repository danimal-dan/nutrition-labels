class Settings {
  private readonly storage = window.localStorage
  private readonly CHILD_NAME_LOCAL_STORAGE_KEY = 'nutrition-labels-child-name'
  private readonly AVERY_TEMPLATE_LOCAL_STORAGE_KEY = 'nutrition-labels-avery-template'
  private readonly DEFAULT_AVERY_TEMPLATE = 4224

  public getChildName(): string {
    return this.storage.getItem(this.CHILD_NAME_LOCAL_STORAGE_KEY) ?? ''
  }

  public setChildName(childName: string) {
    this.storage.setItem(this.CHILD_NAME_LOCAL_STORAGE_KEY, childName)
  }

  public getAveryTemplate(): number {
    const localStorageValue = this.storage.getItem(this.AVERY_TEMPLATE_LOCAL_STORAGE_KEY)

    return localStorageValue ? parseInt(localStorageValue) : this.DEFAULT_AVERY_TEMPLATE
  }

  public setAveryTemplate(averyTemplate: number) {
    this.storage.setItem(this.AVERY_TEMPLATE_LOCAL_STORAGE_KEY, averyTemplate.toString())
  }

  public getAveryTemplateOptions(): number[] {
    return [4224, 5160, 5161, 5163, 5167, 5371]
  }
}

export const useSettings = () => new Settings()
