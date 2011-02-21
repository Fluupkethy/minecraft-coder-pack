package MCP.mod_jumpblock;

import MCP.ApiController;
import MCP.ApiCraftMgr;
import MCP.Mod;
import net.minecraft.src.Block;
import net.minecraft.src.Entity;
import net.minecraft.src.EntityPlayer;
import net.minecraft.src.ItemStack;

public class mod_jumpblock extends Mod
{
	private long tickCounter;
	private BlockJump blockJump;

	/**********************************************************************
	 * 
	 */
	public mod_jumpblock(ApiController ctrl)
	{
		super(ctrl);
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public String getModName()
	{
		return "Jump Block";
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public String getModAuthor()
	{
		return "Cryect";
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public String getModDescription()
	{
		String desc = "Based on the tutorial from Cryect.";
		desc += "\nMod system conversion by Searge.";
		return desc;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onMinecraftStarted()
	{
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onMinecraftEnding()
	{
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onGameStarted()
	{
		this.tickCounter = 1;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onGameEnding()
	{
		this.tickCounter = 0;
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public void onTick()
	{
		if(this.tickCounter > 0)
			++this.tickCounter;
		
		if(this.tickCounter == 95)
		{
			api().printc("\247aWelcome to \247cJump Block \247eby Cryect & Searge.");
		}
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onRegisterBlocksAndItems()
	{
		this.blockJump = new BlockJump(api());
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public void onRegisterRecipes(ApiCraftMgr craftMgr)
	{
        // Sets the recipe be two planks horizontal to each other
        craftMgr.addRecipe(new ItemStack(this.blockJump, 1), new Object[] {
            "##", Character.valueOf('#'), Block.planks
        });
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onConsoleCommand(String command, String param)
	{
		return false;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onKeyPress(int keycode, boolean pressed)
	{
		return false;
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public int onAddFuel(int itemID)
	{
		return 0;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onEntityLeftClick(EntityPlayer player, Entity entity, ItemStack withItem)
	{
		return false;
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onEntityRightClick(EntityPlayer player, Entity entity, ItemStack withItem)
	{
		return false;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onBlockLeftClick(EntityPlayer player, Block block, int x, int y, int z, int side, ItemStack withItem)
	{
		return false;
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onBlockRightClick(EntityPlayer player, Block block, int x, int y, int z, int side, ItemStack withItem)
	{
		return false;
	}
}
